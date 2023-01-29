from fastapi import APIRouter
from api.user.login import get_token_data


router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/login")
async def LoginUser():
    a = get_token_data()
    return a