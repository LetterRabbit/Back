from fastapi import APIRouter, Request, Response, Header, Depends
from api.user.login import get_token_data, gretting_user
from sqlalchemy.orm import Session
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