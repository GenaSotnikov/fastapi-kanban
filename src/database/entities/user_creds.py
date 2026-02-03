from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from entities.user import UserCredentials as UserCredentialsBase


class UserCredentials(UserCredentialsBase, SQLModel, table=True):
    id: UUID | None = Field(primary_key=True, index=True, default_factory=uuid4)
    user_id: UUID = Field(index=True, foreign_key="user.id")