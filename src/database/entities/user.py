from sqlmodel import SQLModel, Field
from src.entities.user import User as UserBase


class User(UserBase, SQLModel, table=True):
    id: str | None = Field(primary_key=True, index=True)

