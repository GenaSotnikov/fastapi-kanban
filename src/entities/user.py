from enum import Enum
from typing import Optional

class UserCredentials:
    id: str
    username: str
    password: str
    user_id: str

    def __init__(self, username: str, password: str, user_id: str):
        self.username = username
        self.password = password
        self.user_id = user_id

class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"

class User:
    id: str
    email: str
    full_name: str
    role: UserRole
    is_active: bool

    def __init__(self, email: str, full_name: str, role: UserRole, is_active: bool):
        self.email = email
        self.full_name = full_name
        self.role = role
        self.is_active = is_active

class CreateUserRequest:
    email: str
    full_name: str
    username: str
    password: str