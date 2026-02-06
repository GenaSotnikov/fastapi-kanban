import copy
import unittest
from uuid import uuid4

from src.entities.user import User, UserRole
from tests.unit.mocks.user_repository_mock import db_mock


uuid_mock = uuid4()
user_mock = User(
                id=uuid_mock, 
                email="test@example.com", 
                full_name="Test User", 
                role=UserRole.USER, 
                is_active=True
            )

class TestCaseWithUserMock(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        db_mock.data.clear()
        self.saved_user = copy.copy(user_mock)
        db_mock.insert(self.saved_user)