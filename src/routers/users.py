from typing import Annotated
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer

from infrastructure.services.jwt import JwtDecodeResStatus, JwtService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def is_authenticated(
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_service: Annotated[JwtService, Depends()],
):
    decode_res = jwt_service.decode(token)

    match decode_res.status:
        case JwtDecodeResStatus.INVALID_TOKEN:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        case JwtDecodeResStatus.SERVER_ERROR:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=decode_res.error_text or "An error occurred while decoding the token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        case JwtDecodeResStatus.SUCCESS:
            return True

# Placeholder for actual authentication logic
    return False

router = APIRouter(prefix="/users", tags=["Users"], dependencies=[Depends(is_authenticated)])

@router.get("/me")
async def read_current_user():
    return {"message": "Current user endpoint"}

@router.get("/{user_id}")
async def read_user(user_id: str):
    return {"message": f"User endpoint for user {user_id}"}
