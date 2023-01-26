import requests
from fastapi import Depends
from core.database import get_db
from db import users
from schemas import users
from sqlalchemy.orm import Session

# def create_user(db : Session, user : users.UserCreate):
#     db_user = users.User(
#         username = user.username,
#         email = user.email,
#         gender = user.gender,
#         age_range = user.age_range,
#         birthday = user.birthday
#     )

#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return 0


def get_token_data():
    url = "https://kapi.kakao.com/v2/user/me"
    headers = {"Authorization" : "Bearer "+'AJJRVjgnWGcdbDGqEGaqcP5Bbtgt204i_tiSPze4CiolUgAAAYXsn0Qg', 'Content-Type': 'application/x-www-form-urlencoded'}
    user_data = requests.get(url=url, headers=headers)
    print(1)
    return user_data


# def login_user(
#     user_create : users.UserCreate,
#     db : Session = Depends(get_db)
# ):
#     return "Hello User"


# print()