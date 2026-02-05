from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4
from config import get_env
import jwt

valid_jti = set() # it's better to save it in Redis for validation

"""
class JwtHeaders:
    Стандартные поля Header (Заголовок)
    В заголовке обычно указываются метаданные для обработки токена: 
    alg — алгоритм подписи (например, HS256, RS256).
    typ — тип токена, почти всегда равен JWT.
    kid (Key ID) — идентификатор ключа, используемого для проверки подписи. 
    alg = get_env('JWT_ALGORITHM')
    typ = 'JWT'
    kid = 'default_key_id'
"""

class JwtTokenData:
    """
    Стандартные поля Payload (Claims)
    iss (Issuer) — издатель токена (например, адрес сервера аутентификации).
    sub (Subject) — субъект токена, обычно уникальный идентификатор пользователя (ID).
    aud (Audience) — аудитория, для которой предназначен токен (ID или URL сервиса-получателя).
    exp (Expiration Time) — время истечения срока действия токена в формате Unix Timestamp.
    nbf (Not Before) — время, раньше которого токен считается недействительным.
    iat (Issued At) — время выпуска токена.
    jti (JWT ID) — уникальный идентификатор самого токена (используется для предотвращения повторного использования). 
    """
    iss = get_env('JWT_ISSUER')
    def __init__(self, user_id: UUID, client_id: str | None = None):
        exp_afer_min = get_env('JWT_EXPIRES_AFTER_MIN')
        if exp_afer_min is None:
            raise BaseException('JWT_EXPIRES_AFTER_MIN must be set')
        self.sub = str(user_id)
        self.exp = datetime.now(timezone.utc) + timedelta(minutes=int(exp_afer_min))
        self.nbf = datetime.now(timezone.utc)
        self.iat = datetime.now(timezone.utc)
        self.jti = str(uuid4())
        valid_jti.add(self.jti)
        self.aud = client_id

class JwtService:
    secret = get_env('JWT_SECRET')
    algorithm = get_env('JWT_ALGORITHM')
    axpires_afer_min = get_env('JWT_EXPIRES_AFTER_MIN')

    def __init__(self):
        if self.secret is None:
            raise BaseException('JWT_SECRET must be set')
        if self.algorithm is None:
            raise BaseException('JWT_ALGORITHM must be set')
        if self.axpires_afer_min is None:
            raise BaseException('JWT_EXPIRES_AFTER_MIN must be set')
        
    def encode(self, user_id: UUID, client_id: str | None = None) -> str:
        token_data = JwtTokenData(user_id, client_id)
        encoded_jwt = jwt.encode(token_data.__dict__, self.secret, algorithm=self.algorithm)
        return encoded_jwt
"""
def decode(self, token: str):
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm if self.algorithm else ''])
            username = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except jwt.InvalidTokenError:
            raise credentials_exception
        user = get_user(fake_users_db, username=token_data.username)
        if user is None:
            raise credentials_exception
        return user
"""    
    