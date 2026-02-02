from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me")
async def read_current_user():
    return {"message": "Current user endpoint"}

@router.get("/{user_id}")
async def read_user(user_id: str):
    return {"message": f"User endpoint for user {user_id}"}