import requests, json, os, uuid
from fastapi import Depends, HTTPException, status
from models.models  import MailBox
from schemas import mailbox_schemas
from sqlalchemy.orm import Session
from models.models import User, MailBoxPosition

from sqlalchemy.orm.exc import NoResultFound

def create_my_mailbox(db : Session, mailbox_data : mailbox_schemas.MailboxBase ):
    print('create_my_mailbox 작동')

    try:
        # 쿼리문으로 데이터 베이스 조회(User, MailBoxPosition)
        owner_q = db.query(User).filter(User.id == mailbox_data.owner_id)
        if not owner_q.first():
            raise Exception 
        owner_id = mailbox_data.owner_id

        mailbox_position_q = db.query(MailBoxPosition).filter(MailBoxPosition.id == mailbox_data.mailbox_position_id)
        if not mailbox_position_q.first():
            raise Exception
        mailbox_position_id = mailbox_data.mailbox_position_id
        
        # 주소는 uuid4 사용.
        address = str(uuid.uuid4())

        # 편지함 이름
        if mailbox_data.name == "":
            name = owner_q.first().username
        else:
            name = mailbox_data.name

        new_mailbox = MailBox(
            owner_id = owner_id,
            mailbox_position_id = mailbox_position_id,
            address = address,
            name = name
        )

        db.add(new_mailbox)
        db.commit()
        db.refresh(new_mailbox)

    except Exception:
        raise HTTPException(status_code=404, detail= "Key value that does not exist.")