from fastapi import APIRouter, Request, Response, Header
from api.user.login import get_token_data

from typing import Optional

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/login")
async def LoginUser(
    authCode: Optional[str] = Header(None)
):
    a = get_token_data(authCode)
    return a