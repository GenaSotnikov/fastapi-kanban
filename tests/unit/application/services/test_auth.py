from uuid import uuid4
from src.application.services.auth import AuthorizationService, CheckUserResult
from src.infrastructure.services.auth import hash_service
from tests.unit.mocks.user_repository_mock import repository_with_mock_db_session
from tests.unit.utils.test_case_with_user_mock import TestCaseWithUserMock

authService = AuthorizationService(user_repository=repository_with_mock_db_session, hash_service=hash_service)

class TestAuthService(TestCaseWithUserMock):
    not_saved_user_id = uuid4()
    def setUp(self) -> None:
        return super().setUp()

    def test_check_user(self):
        res = authService.check_user(self.saved_user.id)
        self.assertEqual(res, CheckUserResult.USER_OK)
        res = authService.check_user(self.not_saved_user_id)
        self.assertEqual(res, CheckUserResult.USER_NOT_FOUND)
        self.saved_user.is_active = False
        res = authService.check_user(self.saved_user.id)
        self.assertEqual(res, CheckUserResult.USER_INACTIVE)