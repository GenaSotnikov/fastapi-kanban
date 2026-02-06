from uuid import uuid4
from tests.unit.mocks.user_repository_mock import repository_with_mock_db_session
from tests.unit.utils.test_case_with_user_mock import TestCaseWithUserMock


class TestUserRepository(TestCaseWithUserMock):
    def setUp(self) -> None:
        super().setUp()
    
    def test_get_user_by_id(self):
        user = repository_with_mock_db_session.get_by_id(self.saved_user.id)
        self.assertIsNotNone(user)
        # always true
        if user is not None:
            self.assertEqual(user.id, self.saved_user.id)
            self.assertEqual(user.email, self.saved_user.email)
            self.assertEqual(user.full_name, self.saved_user.full_name)
            self.assertEqual(user.role, self.saved_user.role)
            self.assertEqual(user.is_active, self.saved_user.is_active)
        not_existing_user = repository_with_mock_db_session.get_by_id(uuid4())
        self.assertIsNone(not_existing_user)
