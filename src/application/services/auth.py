from dataclasses import dataclass
from typing import Annotated, Callable, Optional

from fastapi import Depends

from database.engine import DatabaseConnection
from entities.user import CreateUserRequest
from enum import Enum
from pwdlib import PasswordHash

from infrastructure.repositories.user import UserRepository

class LoginStatuses(Enum):
    SUCCESS = "success"
    INVALID_CREDENTIALS = "invalid_credentials"
    CREDENTIALS_NOT_FOUND = "credentials_not_found"
    USER_NOT_FOUND = "user_not_found"
    USER_INACTIVE = "user_inactive"

class RegisterStatuses(Enum):
    SUCCESS = "success"
    USER_ALREADY_EXISTS = "user_already_exists"
    ERROR = "error"
    NOT_CREATED = "not_created"

@dataclass
class RegisterResult:
    status: RegisterStatuses
    errorText: Optional[str] = None

type HashFunction = Callable[[str], str]

class AuthorizationService:
    def __init__(self, user_repository: UserRepository, hash_function: HashFunction):
        self.user_repository = user_repository
        self.hash_function = hash_function

    async def login(self, username: str, password: str) -> LoginStatuses:
        user = self.user_repository.get_by_username(username)

        if user is None or user.id is None:
            return LoginStatuses.USER_NOT_FOUND
        if user.is_active is False:
            return LoginStatuses.USER_INACTIVE

        user_creds = self.user_repository.get_credentials_by_user_id(user.id)

        if user_creds is None: 
            return LoginStatuses.CREDENTIALS_NOT_FOUND
        
        pass_hash = self.hash_function(password)

        if user_creds.password != pass_hash:
            return LoginStatuses.INVALID_CREDENTIALS
        
        return LoginStatuses.SUCCESS

    async def register(self, createUserRequest: CreateUserRequest) -> RegisterResult:
        try:
            existing_user = self.user_repository.get_by_username(createUserRequest.username)

            if existing_user is not None:
                return RegisterResult(
                    status=RegisterStatuses.USER_ALREADY_EXISTS,
                    errorText="User with this username already exists"
                )
            
            createUserRequest.password = self.hash_function(createUserRequest.password)

            new_user = await self.user_repository.create_user(createUserRequest)
            if new_user is None:
                return RegisterResult(
                    status=RegisterStatuses.NOT_CREATED,
                    errorText="Failed to create user"
                )

            return RegisterResult(status=RegisterStatuses.SUCCESS)
        except BaseException as e:
            return RegisterResult(
                status=RegisterStatuses.ERROR,
                errorText=str(e)
            )


password_hash = PasswordHash.recommended()
hash_fun: HashFunction = password_hash.hash

def get_auth_service(db_session: Annotated[DatabaseConnection, Depends()]): 
    repository = UserRepository(db_session)
    return AuthorizationService(repository, hash_fun)
