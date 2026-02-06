from src.infrastructure.repositories.user import UserRepository
from .engine_mock import db_mock

repository_with_mock_db_session = UserRepository(db_mock)
