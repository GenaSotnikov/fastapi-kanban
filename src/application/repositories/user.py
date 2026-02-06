from abc import ABC, abstractmethod
from uuid import UUID
from entities.user import CreateUserRequest, User, UserCredentials


class UserRepository(ABC):
    @abstractmethod
    def get_by_username(self, username: str) -> User | None:
        pass

    @abstractmethod
    def get_credentials_by_user_id(self, user_id: UUID) -> UserCredentials | None:
        pass
    
    @abstractmethod
    async def create_user(self, request: CreateUserRequest) -> User | None:
        pass

    @abstractmethod
    def get_by_id(self, user_id: UUID) -> User | None:
        pass