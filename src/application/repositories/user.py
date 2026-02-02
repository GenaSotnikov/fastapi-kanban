from entities.user import CreateUserRequest, User, UserCredentials, UserRole
from collections.abc import Awaitable
from .db_session import DatabaseSession

class UserRepository:
    def __init__(self, database_session: DatabaseSession):
        self.database_session = database_session

    def get_by_username(self, username: str) -> Awaitable[User | None]:
        return self.database_session.select(User, {"username": username})

    def get_credentials_by_user_id(self, user_id: str) -> Awaitable[UserCredentials | None]:
        return self.database_session.select(UserCredentials, {"id": user_id})

    async def create_user(self, request: CreateUserRequest) -> User | None:
        user_data = User(
            email=request.email,
            full_name=request.full_name,
            role=UserRole.USER,
            is_active=True
        )
        new_user = await self.database_session.insert(User, user_data)
        if new_user is None:
            raise KeyError('Failed to create user')

        creds_data = UserCredentials(
            username=request.username,
            password=request.password,
            user_id=new_user.id
        )
        new_creds = await self.database_session.insert(UserCredentials, creds_data)
        if new_creds is None:
            raise KeyError('Failed to create user credentials')

        return new_user