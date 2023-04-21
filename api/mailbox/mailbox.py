import requests, json, os, uuid
from fastapi import Depends, HTTPException, status
from schemas import mailbox_schemas
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.models import User, MailBoxPosition, Letter, MailBox

from sqlalchemy.orm.exc import NoResultFound
from core.log import LOG

def create_my_mailbox(db : Session, mailbox_data : mailbox_schemas.MailboxBase ):
    print('create_my_mailbox 작동')

    try:
        # 쿼리문으로 데이터 베이스 조회(User, MailBoxPosition)
        target_user = db.query(User).filter(User.id == mailbox_data.owner_id).first()
        if not target_user:
            raise KeyError 
        user_id = mailbox_data.owner_id

        if not db.query(MailBoxPosition).filter(MailBoxPosition.id == mailbox_data.mailbox_position_id).first():
            raise KeyError
        mailbox_position_id = mailbox_data.mailbox_position_id
        
        # 편지함 중복생성 방지.
        if db.query(MailBox).filter(MailBox.owner_id == user_id).first() is not None:
            raise KeyError

        # 주소는 uuid4 사용.
        address = str(uuid.uuid4())

        # 편지함 이름
        if mailbox_data.name == "":
            name = target_user.username
        else:
            name = mailbox_data.name

        new_mailbox = MailBox(
            owner_id = user_id,
            mailbox_position_id = mailbox_position_id,
            address = address,
            name = name
        )

        db.add(new_mailbox)
        db.commit()
        db.refresh(new_mailbox)

    except KeyError:
        LOG.error(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Key value that does not exist.")
    except Exception as e:
        LOG.error(str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "[create_my_mailbox error] : "+ str(e))
    
def open_my_mailbox(db : Session, data):
    print('open_my_mailbox 작동')
    try:
        user_id = data.id
        target_mailbox_id = db.query(MailBox.id).filter(MailBox.owner_id == user_id).scalar()
        rows = db.query(
            Letter.id, 
            Letter.username, 
            Letter.description, 
            func.DATE_FORMAT(Letter.created_at, '%Y-%m-%d').label('created_date')
        ).filter(Letter.mailbox_id == target_mailbox_id).all()

        result = [{key: value for key, value in zip(row.keys(), row)} for row in rows]

        return result
    
    except Exception as e :
        LOG.error(str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "open_my_mailbox error" + str(e))
    
def open_my_letter(db : Session, data, letter_id):
    try:
        user_id = data.id
        target_mailbox_id = db.query(MailBox.id).filter(MailBox.owner_id == user_id).scalar()
        letters = db.query(
            Letter.id, 
            Letter.username, 
            Letter.description, 
            func.DATE_FORMAT(Letter.created_at, '%Y-%m-%d').label('created_date')
            ).filter(
                Letter.id == letter_id,
                Letter.mailbox_id == target_mailbox_id
            ).one()
        
        return letters
    except NoResultFound as e:
        LOG.error(str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "NoResultFound " +": " + str(e))
    except Exception as e :
        LOG.error(str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "open_my_mailbox error" + str(e))