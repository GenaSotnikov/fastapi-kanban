from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from config import get_env
import jwt

valid_jti = set() # it's better to save it in Redis for validation
jwt_issuer = get_env('JWT_ISSUER')

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


@dataclass
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
    sub: str
    iss: str | None
    aud: str | None
    exp: datetime
    nbf: datetime
    iat: datetime
    jti: str

    @classmethod
    def build(cls, user_id: UUID, client_id: str | None = None) -> 'JwtTokenData':
        exp_afer_min = get_env('JWT_EXPIRES_AFTER_MIN')
        if exp_afer_min is None:
            raise BaseException('JWT_EXPIRES_AFTER_MIN must be set')

        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(minutes=int(exp_afer_min))
        jti = str(uuid4())
        valid_jti.add(jti)

        return cls(
            sub=str(user_id),
            iss=jwt_issuer,
            aud=client_id,
            exp=expires_at,
            nbf=now,
            iat=now,
            jti=jti,
        )

    def to_payload(self) -> dict:
        return {
            "sub": self.sub,
            "iss": self.iss,
            "aud": self.aud,
            "exp": int(self.exp.timestamp()),
            "nbf": int(self.nbf.timestamp()),
            "iat": int(self.iat.timestamp()),
            "jti": self.jti,
        }

    @classmethod
    def from_payload(cls, payload: dict) -> 'JwtTokenData':
        required_fields = ("sub", "exp", "nbf", "iat", "jti")
        missing = [field for field in required_fields if field not in payload]
        if missing:
            raise ValueError(f"Missing fields in JWT payload: {', '.join(missing)}")

        return cls(
            sub=str(payload["sub"]),
            iss=payload.get("iss"),
            aud=payload.get("aud"),
            exp=cls._coerce_datetime(payload["exp"]),
            nbf=cls._coerce_datetime(payload["nbf"]),
            iat=cls._coerce_datetime(payload["iat"]),
            jti=str(payload["jti"]),
        )

    @staticmethod
    def _coerce_datetime(value: Any) -> datetime:
        if isinstance(value, datetime):
            if value.tzinfo is None:
                return value.replace(tzinfo=timezone.utc)
            return value
        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(value, timezone.utc)
        raise ValueError("Invalid datetime value in JWT payload")

class JwtDecodeResStatus(Enum):
    INVALID_TOKEN = "invalid_token"
    SERVER_ERROR = "server_error"
    SUCCESS = "success"

@dataclass
class DecodeJwtRes:
    token_data: JwtTokenData | None = None
    status: JwtDecodeResStatus | None = None
    error_text: str | None = None

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
        token_data = JwtTokenData.build(user_id, client_id)
        encoded_jwt = jwt.encode(token_data.to_payload(), self.secret, algorithm=self.algorithm)
        return encoded_jwt

    def decode(self, token: str, audience: str | None = None) -> DecodeJwtRes:
        try:
            payload = jwt.decode(token, self.secret, audience=audience, algorithms=[self.algorithm if self.algorithm else ''])
            token_data = JwtTokenData.from_payload(payload)
            return DecodeJwtRes(token_data=token_data, status=JwtDecodeResStatus.SUCCESS)
        except jwt.InvalidTokenError:
                return DecodeJwtRes(status=JwtDecodeResStatus.INVALID_TOKEN)
        except ValueError as e:
                return DecodeJwtRes(status=JwtDecodeResStatus.SERVER_ERROR, error_text=str(e))
        except BaseException as e:
                return DecodeJwtRes(status=JwtDecodeResStatus.SERVER_ERROR, error_text=str(e))
