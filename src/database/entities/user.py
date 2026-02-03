from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from entities.user import User as UserBase


class User(UserBase, SQLModel, table=True):
    id: UUID | None = Field(primary_key=True, index=True, default_factory=uuid4)

