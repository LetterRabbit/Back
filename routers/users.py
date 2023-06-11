import requests
import os
from fastapi import APIRouter, Request, Response, HTTPException, Header, Depends,Cookie, status, Cookie
from api.user.login import create_user,get_token_data, get_dev_token_data
from api.user.qr import save_aws_s3
from fastapi.responses import JSONResponse
from core.decoration import get_user_from_jwt
from sqlalchemy.orm import Session
from sqlalchemy import MetaData, Table
from core import database
from typing import Optional
from schemas import user_schemas
from models import models
from core.log import LOG
from models.models  import MailBox

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
    authCode: str = Header(None, description="Token for authentication with Kakao API")
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
    token, user = create_user(db = db, user = user)
    data = {
        "access_token" : token,
    }
    return JSONResponse(content=data, status_code=200)

   except Exception as e:
       LOG.error(str(e))
       return HTTPException(
           status_code=401,
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
    token, user = create_user(db = db, user = user)
    data = {
        "access_token" : token,
        }
    # response.set_cookie(key = "access_token", value=token, secure=True, httponly=True)
    return JSONResponse(content=data, status_code=200)


@router.get('/callback')
async def kakaoAuth(response: Response, code: Optional[str]="NONE",    db : Session = Depends(database.get_db),):
    _url = f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={KAKAO_REST_API_KEY}&code={code}&redirect_uri={REDIRECT_URI}'
    _res = requests.post(_url)
    _result = _res.json()
    response.set_cookie(key="authCode", value=_result['access_token'])
    return 200


@router.get("/me")
async def check_user_data(
    request : Request,
    db : Session = Depends(database.get_db),
    access : Optional[str] = Header(None)
):
    #print("header>>>>>",request.headers)
    #print("cookie>>>>>", request.cookies.get('access_token'))
    #print(request.headers.items())
    #token = request.headers.get('access_token')
    user_info = get_user_from_jwt(access_token = access, db=db)

    return user_info

@router.get('/qr')
async def check_user_qr(
    request : Request,
    db : Session = Depends(database.get_db),
    access : Optional[str] = Header(None)
    ):
    try:
        user_info = get_user_from_jwt(access, db=db)
        data = db.query(models.MailBox).filter(models.MailBox.owner_id == user_info.id).first()
        url = f"{request.base_url}mailbox/{data.address}"
        url_qr = save_aws_s3(url, user_info.id)
        mytable = Table('users', MetaData(), autoload=True, autoload_with=database.engine)
        qr = mytable.update().where(mytable.c.id == user_info.id).values(self_domain = url, qr_code = url_qr)
        database.engine.execute(qr)
        return JSONResponse(content={"self_domain" : user_info.self_domain, "qr_domain" : user_info.qr_code}, status_code=201)

    except Exception as e:
        LOG.error(str(e))
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
             detail=str(e)
        )
