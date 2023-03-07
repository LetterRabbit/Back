import os
from jose import jwt
from jose.exceptions import ExpiredSignatureError
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import models

secretkey = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")

def get_user_from_jwt(access_token, db : Session):
    try:
        data = jwt.decode(token=access_token,algorithms=algorithm,key=secretkey)
        if db.query(models.User).filter(models.User.id == data['id']).first() is None:
            raise Exception
        data = db.query(models.User).filter(models.User.id == data['id']).first()
        return data
    
    except ExpiredSignatureError:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= str(e)                 )
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    



