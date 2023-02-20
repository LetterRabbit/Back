from fastapi import APIRouter, Request, Response, HTTPException, Header, Depends,Cookie, status
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
    response: Response,
    db : Session = Depends(database.get_db),
    authCode: Optional[str] = Header(None)
):
    try:
        user_create = get_token_data(authCode)
        user = user_schemas.UserCreate(
            username = user_create["username"],
            email = user_create["email"],
            birthday = user_create["birthday"],
            gender = user_create["gender"],
            age_range = user_create["age_range"]
        )
        token = create_user(db = db, user = user)
        print(token)
        response.set_cookie(key = "access_token", value=token, secure=True, httponly=True)
        return token
    
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
             detail=str(e)
        )  
    
@router.post('/logout')
async def logout(
    response : Response,
    access_token : Optional[str] = Cookie(None),
):
    try:
        response.delete_cookie(key="access_token", value = access_token ,secure=True,httponly=True)
    
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
             detail=str(e)
        )  