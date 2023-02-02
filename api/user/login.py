import requests
from fastapi import Depends
from core.database import get_db
from db import users
from schemas import users
from sqlalchemy.orm import Session

HOST = "kapi.kakao.com"

def create_user(db : Session, user : users.UserCreate):
    db_user = users.User(
        username = user.username,
        email = user.email,
        gender = user.gender,
        age_range = user.age_range,
        birthday = user.birthday
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return 0


def get_token_data(authCode):
    url = 'https://oauth2.googleapis.com/tokeninfo?id_token='
    response = requests.get(url+authCode)
    user_info = response.json()
    return user_info