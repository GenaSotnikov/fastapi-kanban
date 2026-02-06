from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from application.services.hash import HashService
from entities.user import CreateUserRequest
from enum import Enum

from application.repositories.user import UserRepository

class LoginStatuses(Enum):
    SUCCESS = "success"
    INVALID_CREDENTIALS = "invalid_credentials"
    CREDENTIALS_NOT_FOUND = "credentials_not_found"
    USER_NOT_FOUND = "user_not_found"
    USER_INACTIVE = "user_inactive"
    ERROR = "error"

class RegisterStatuses(Enum):
    SUCCESS = "success"
    USER_ALREADY_EXISTS = "user_already_exists"
    ERROR = "error"
    NOT_CREATED = "not_created"

@dataclass
class LoginResult:
    status: LoginStatuses
    errorText: Optional[str] = None
    user_id: Optional[UUID] = None

@dataclass
class RegisterResult:
    status: RegisterStatuses
    errorText: Optional[str] = None

class CheckUserResult(Enum):
    USER_OK = "user_ok"
    USER_NOT_FOUND = "user_not_found"
    USER_INACTIVE = "user_inactive"
    ERROR = "error"

class AuthorizationService:
    def __init__(self, user_repository: UserRepository, hash_service: HashService):
        self.user_repository = user_repository
        self.hash_function = hash_service.hash_fun
        self.verify_hash = hash_service.verify

    def login(self, username: str, password: str) -> LoginResult:
        try:
            user = self.user_repository.get_by_username(username)

            if user is None or user.id is None:
                return LoginResult(LoginStatuses.USER_NOT_FOUND)
            if user.is_active is False:
                return LoginResult(LoginStatuses.USER_INACTIVE)

            user_creds = self.user_repository.get_credentials_by_user_id(user.id)

            if user_creds is None: 
                return LoginResult(LoginStatuses.CREDENTIALS_NOT_FOUND)
            
            if not self.verify_hash(password, user_creds.password):
                return LoginResult(LoginStatuses.INVALID_CREDENTIALS)
            
            return LoginResult(LoginStatuses.SUCCESS, user_id=user.id)
        except BaseException as e:
            return LoginResult(LoginStatuses.ERROR, str(e))

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

    def check_user(self, user_id: UUID) -> CheckUserResult:
        user = self.user_repository.get_by_id(user_id)
        if user is None:
            return CheckUserResult.USER_NOT_FOUND
        if not user.is_active:
            return CheckUserResult.USER_INACTIVE
        return CheckUserResult.USER_OK
