import unittest
from uuid import uuid4
from src.infrastructure.services.jwt import JwtDecodeResStatus, JwtService

jwtService = JwtService()

class TestJwtService(unittest.TestCase):
    def test_jwt_service_init(self):
        self.assertIsNotNone(jwtService.secret)
        self.assertIsNotNone(jwtService.algorithm)
        self.assertIsNotNone(jwtService.axpires_afer_min)

    def test_jwt_encode_decode(self):
        user_id = uuid4()
        token = jwtService.encode(user_id, client_id="test_client")
        self.assertIsNotNone(token)
        token2 = jwtService.encode(user_id, client_id="test_client")
        self.assertNotEqual(token, token2) # jti is different
        
        decoded_token = jwtService.decode(token2, audience="test_client")
        self.assertIsNone(decoded_token.error_text)
        self.assertIsNotNone(decoded_token)
        self.assertEqual(decoded_token.status, JwtDecodeResStatus.SUCCESS)
        self.assertIsNotNone(decoded_token.token_data)
        if decoded_token.token_data:
            self.assertEqual(decoded_token.token_data.sub, str(user_id))
            self.assertEqual(decoded_token.token_data.aud, "test_client")
            self.assertTrue(decoded_token.token_data.jti)
