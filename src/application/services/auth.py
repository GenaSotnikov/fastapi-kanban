from typing import Callable
from ..repositories.user import UserRepository
from entities.user import CreateUserRequest
from enum import Enum

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

type HashFunction = Callable[[str], str]

class AuthorizationService:
    def __init__(self, user_repository: UserRepository, hash_function: HashFunction):
        self.user_repository = user_repository
        self.hash_function = hash_function

    async def login(self, username: str, password: str) -> LoginStatuses:
        user = await self.user_repository.get_by_username(username)

        if user is None:
            return LoginStatuses.USER_NOT_FOUND
        if user.is_active is False:
            return LoginStatuses.USER_INACTIVE

        user_creds = await self.user_repository.get_credentials_by_user_id(user.id)

        if user_creds is None: 
            return LoginStatuses.CREDENTIALS_NOT_FOUND
        
        pass_hash = self.hash_function(password)

        if user_creds.password != pass_hash:
            return LoginStatuses.INVALID_CREDENTIALS
        
        return LoginStatuses.SUCCESS

    async def register(self, createUserRequest: CreateUserRequest) -> RegisterStatuses:
        try:

            existing_user = await self.user_repository.get_by_username(createUserRequest.username)
            if existing_user is not None:
                return RegisterStatuses.USER_ALREADY_EXISTS
            
            createUserRequest.password = self.hash_function(createUserRequest.password)

            new_user = await self.user_repository.create_user(createUserRequest)
            return RegisterStatuses.SUCCESS if new_user is not None else RegisterStatuses.NOT_CREATED
        except KeyError:
            return RegisterStatuses.ERROR
    