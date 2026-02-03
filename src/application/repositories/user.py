from abc import ABC, abstractmethod
from typing import Awaitable
from entities.user import CreateUserRequest, User, UserCredentials


class UserRepository(ABC):
    @abstractmethod
    def get_by_username(self, username: str) -> Awaitable[User | None]:
        pass

    @abstractmethod
    def get_credentials_by_user_id(self, user_id: str) -> Awaitable[UserCredentials | None]:
        pass
    
    @abstractmethod
    async def create_user(self, request: CreateUserRequest) -> User | None:
        pass