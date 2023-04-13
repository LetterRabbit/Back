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
        print(data)        
        if db.query(models.User).filter(models.User.id == data['id']).first() is None:
            raise Exception
        user = db.query(models.User).filter(models.User.id == data['id']).first()
        return user
    
    except ExpiredSignatureError as a:
        raise HTTPException(status_code=400, detail=str(a))
    

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= str(e))
    



