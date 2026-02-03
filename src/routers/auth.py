from typing import Annotated
from fastapi import APIRouter
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from entities.user import CreateUserRequest as CreateUserRequestBase
from application.services.auth import (
    get_auth_service,
    AuthorizationService,
    RegisterStatuses,
)

class CreateUserRequest(CreateUserRequestBase, BaseModel):
    pass

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return {"message": "Login endpoint"}

@router.post("/register")
async def register(payload: CreateUserRequest, authService: Annotated[AuthorizationService, Depends(get_auth_service)]):
    registration_res = await authService.register(payload)

    match(registration_res.status):
        case RegisterStatuses.SUCCESS:
            return { 'success': True }
        case RegisterStatuses.USER_ALREADY_EXISTS:
            raise HTTPException(400, { 'success': False, 'reason': registration_res.errorText or registration_res.status.value })
        case RegisterStatuses.ERROR | RegisterStatuses.NOT_CREATED:
            raise HTTPException(500, { 'success': False, 'reason': registration_res.errorText or registration_res.status.value })
