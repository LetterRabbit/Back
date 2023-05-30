import requests, json, os
from fastapi import Depends, HTTPException, status
from core.database import get_db
from models.models  import User
from schemas import user_schemas
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from jose import jwt
from datetime import datetime, timedelta
from core.log import LOG

KAKAO_REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")
secretkey = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
REDIRECT_URI = "http://localhost:8000/users/callback"


def connect_kakao_server(authCode):
    try:
        url = "https://kauth.kakao.com/oauth/token"
        header = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "code" : authCode,
            "client_id" : KAKAO_REST_API_KEY,
            "grant_type" : "authorization_code"
            }
        a = requests.post(url=url, headers=header,data=data)
        res = a.json()
        return res
    except Exception as e:
        LOG.error("kakao connect error : ", str(e))
        return HTTPException(
            status_code=400,
            detail=str(e)
        )

def create_access_token(data : dict, expires_delta : timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow()+ expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode, secretkey, algorithm)
    return encoded_jwt


def get_token_data(authCode):
    res = connect_kakao_server(authCode)
    user_data = res['access_token']
    token_type = res['token_type']
    url = 'https://kapi.kakao.com/v2/user/me'
    header = {
        "Authorization" : token_type + " " + user_data
    }
    response = requests.get(url = url, headers=header)
    user_info = response.json()
    data = {
        "username" : user_info['kakao_account']['profile']['nickname'],
        "email" : user_info['kakao_account']['email'],
        "gender" : user_info['kakao_account']['gender'],
        "age_range" : user_info['kakao_account']['age_range'],
        "birthday" : user_info['kakao_account']['birthday']
    }

    return data

def create_user(db : Session, user : user_schemas.UserCreate):
    if db.query(User).filter(User.email == user.email).first() is None:
        db_user = User(
            username = user.username,
            email = user.email,
            gender = user.gender,
            age_range = user.age_range,
            birthday = user.birthday
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        data = db.query(User).filter(User.email == user.email).first()
        token_data = {
            "id" : data.id,
            "username" : data.username,
        }
        token = create_access_token(data=token_data)
        return token
    else:
        data = db.query(User).filter(User.email == user.email).first()
        token_data = {
            "id" : data.id,
            "username" : data.username,
        }
        token = create_access_token(data=token_data)
        return token, data.id
    
def get_dev_token_data(authCode):
    user_data = authCode
    token_type = "Bearer"
    url = 'https://kapi.kakao.com/v2/user/me'
    header = {
        "Authorization" : token_type + " " + user_data
    }
    response = requests.get(url = url, headers=header)
    user_info = response.json()
    data = {
        "username" : user_info['kakao_account']['profile']['nickname'],
        "email" : user_info['kakao_account']['email'],
        "gender" : user_info['kakao_account']['gender'],
        "age_range" : user_info['kakao_account']['age_range'],
        "birthday" : user_info['kakao_account']['birthday']
    }
    return data