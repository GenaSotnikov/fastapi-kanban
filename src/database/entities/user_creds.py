from sqlmodel import SQLModel, Field
from src.entities.user import UserCredentials as UserCredentialsBase


class UserCredentials(UserCredentialsBase, SQLModel, table=True):
    id: str | None = Field(primary_key=True, index=True)