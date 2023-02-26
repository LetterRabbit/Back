import requests,os
from fastapi import APIRouter, Request, Response, HTTPException, Header, Depends,Cookie, status
from api.user.login import create_user,get_token_data, get_dev_token_data
from sqlalchemy.orm import Session
from typing import Optional
from core import database
from schemas import user_schemas
from fastapi.responses import RedirectResponse
from urllib.parse import urlparse, parse_qs



KAKAO_REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")
secretkey = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
REDIRECT_URI = "https://oauth.pstmn.io/v1/callback"
auth_code = ''

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/login")
async def LoginUser(
    response: Response,
    request : Request,
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
     
@router.post('/dev')
def dev_kakao_login(
    response : Response,
    db : Session = Depends(database.get_db),
    authCode: Optional[str] = Header(None)
):
    user_create = get_dev_token_data(authCode=authCode)
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
        
    return 


@router.get('/callback')
async def kakaoAuth(response: Response, code: Optional[str]="NONE",    db : Session = Depends(database.get_db),):
    _url = f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={KAKAO_REST_API_KEY}&code={code}&redirect_uri={REDIRECT_URI}'
    _res = requests.post(_url)
    _result = _res.json()
    # data = {"authCode" : _result['access_token']}
    response.set_cookie(key="authCode", value=_result['access_token'])
    # print(_result)
    # print(_result['access_token'])
    return 200