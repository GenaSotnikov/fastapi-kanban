from typing import Annotated
from fastapi import Depends

from application.services.hash import HashService
from database.engine import DatabaseConnection
from pwdlib import PasswordHash

from src.application.services.auth import AuthorizationService
from src.infrastructure.repositories.user import UserRepository


password_hash = PasswordHash.recommended()
hash_service = HashService(hash_fun=password_hash.hash, verify=password_hash.verify)

def get_auth_service(db_session: Annotated[DatabaseConnection, Depends()]): 
    repository = UserRepository(db_session)
    return AuthorizationService(repository, hash_service)