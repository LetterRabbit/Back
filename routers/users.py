from fastapi import APIRouter
from api.user.login import greeting_user


router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/hello")
async def HelloUser():
    return greeting_user()