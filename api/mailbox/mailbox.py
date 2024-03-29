import requests, json, os, uuid, smtplib
from fastapi import Depends, HTTPException, status
from schemas import mailbox_schemas
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.models import User, MailBoxPosition, Letter, MailBox

from email.mime.text import MIMEText

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import SQLAlchemyError

from core.log import LOG

def create_my_mailbox(db : Session, mailbox_data : mailbox_schemas.MailboxBase ):
    try:
        mailbox_query = db.query(MailBox).filter(MailBox.owner_id == mailbox_data.owner_id).first()
        if mailbox_query:
            return mailbox_query
        else:
            # 쿼리문으로 데이터 베이스 조회(User, MailBoxPosition)
            target_user = db.query(User).filter(User.id == mailbox_data.owner_id).first()
            if not target_user:
                raise KeyError 
            user_id = mailbox_data.owner_id

            if not db.query(MailBoxPosition).filter(MailBoxPosition.id == mailbox_data.mailbox_position_id).first():
                raise KeyError
            mailbox_position_id = mailbox_data.mailbox_position_id

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
            
            return new_mailbox

    except KeyError as e:
        LOG.error(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Key value that does not exist.")
    except Exception as e:
        LOG.error(str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "[create_my_mailbox error] : "+ str(e))
    
def open_my_mailbox(db : Session, data, skip, limit):
    try:
        user_id = data.id
        target_mailbox_id = db.query(MailBox.id).filter(MailBox.owner_id == user_id).scalar()
        
        mailbox_query = db.query(
            Letter.id, 
            Letter.username, 
            Letter.description, 
            func.DATE_FORMAT(Letter.created_at, '%Y-%m-%d').label('created_date')
        ).filter(Letter.mailbox_id == target_mailbox_id)

        print(type(mailbox_query))

        total_count = mailbox_query.count()

        rows = mailbox_query.offset(skip).limit(limit).all()

        result = [{key: value for key, value in zip(row.keys(), row)} for row in rows]

        return {"total_count" : total_count, "result" : result}
    
    except Exception as e :
        LOG.error(str(e))
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "open_my_mailbox error" + str(e))
    
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
        
        total_list= []
        total_list_query = db.query(Letter.id).filter(Letter.mailbox_id == target_mailbox_id).all()

        for (letter_id,) in total_list_query:
            total_list.append(letter_id)
        
        res = {
            "id" : letters.id,
            "username" : letters.username,
            "desc" : letters.description,
            "created_at": letters.created_date, 
            "total_list" : total_list
        }
        
        return res
    except NoResultFound as e:
        LOG.error(str(e))
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "NoResultFound " +": " + str(e))
    except Exception as e :
        LOG.error(str(e))
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "open_my_mailbox error" + str(e))

# async def send_email_async(report_letter):
    

async def get_mailbox_id(user_id: int, db: Session) -> int:
    try:
        mailbox_id = db.query(MailBox.id).filter(MailBox.owner_id == user_id).first()[0]
        return mailbox_id
    except NoResultFound:
        return None
    except SQLAlchemyError as e:
        return None