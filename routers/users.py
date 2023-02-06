from fastapi import APIRouter, Request, Response, Header, Depends
from api.user.login import create_user,get_token_data
from sqlalchemy.orm import Session
from typing import Optional
from core import database
from schemas import user_schemas
router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/login")
async def LoginUser(
    db : Session = Depends(database.get_db),
    authCode: Optional[str] = Header(None)
):
    try:
        print("1")
        user_create = get_token_data(authCode)
        user = user_schemas.UserCreate(
            username = user_create["username"],
            email = user_create["email"],
            birthday = user_create["birthday"],
            gender = user_create["gender"],
            age_range = user_create["age_range"]
        )
        create_user(db = db, user = user)
        return 0
    
    except Exception as e:
        print(str(e))
        return e