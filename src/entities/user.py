from dataclasses import dataclass
from enum import Enum
from uuid import UUID

@dataclass
class UserCredentials:
    id: UUID
    username: str
    password: str
    user_id: UUID

class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"

@dataclass
class User:
    id: UUID
    email: str
    full_name: str
    role: UserRole
    is_active: bool

class CreateUserRequest:
    email: str
    full_name: str
    username: str
    password: str