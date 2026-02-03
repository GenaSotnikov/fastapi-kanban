from collections.abc import Awaitable
from typing import cast
from uuid import UUID

from sqlalchemy import CursorResult

from database.entities.user import User
from database.entities.user_creds import UserCredentials
from entities.user import CreateUserRequest, UserRole
from application.repositories.db_session import DatabaseSession

class UserRepository:
    def __init__(self, database_session: DatabaseSession):
        self.database_session = database_session

    def get_by_username(self, username: str) -> User | None:
        query_res = self.database_session.execute_raw(
            'SELECT * FROM "user" INNER JOIN usercredentials ON "user".id = usercredentials.user_id WHERE usercredentials.username = :username',
            { "username": username },
        )
        typed_query_res = cast(CursorResult, query_res)
        if typed_query_res is None:
            return None
        first_record = typed_query_res.first()
        if first_record is None:
            return None
        return cast(User, first_record._data)

    def get_credentials_by_user_id(self, user_id: UUID) -> UserCredentials | None:
        return self.database_session.select(UserCredentials, {"id": user_id})

    async def create_user(self, request: CreateUserRequest) -> User | None:
        user_data = User(
            id=None,
            email=request.email,
            full_name=request.full_name,
            role=UserRole.USER,
            is_active=True
        )
        new_user = self.database_session.insert(User, user_data)
        if new_user is None or new_user.id is None:
            raise BaseException('Failed to create user')

        creds_data = UserCredentials(
            id=None,
            username=request.username,
            password=request.password,
            user_id=new_user.id
        )
        new_creds = self.database_session.insert(UserCredentials, creds_data)
        if new_creds is None:
            raise BaseException('Failed to create user credentials')

        return new_user
