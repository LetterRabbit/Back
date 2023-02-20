import requests, json, os, uuid
from fastapi import Depends, HTTPException, status
from core.database import get_db
from models.models  import MailBox
from schemas import mailbox_schemas
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from models.models import User, MailBoxPosition

from sqlalchemy.orm.exc import NoResultFound

from datetime import datetime, timedelta

def create_my_mailbox(db : Session, mailbox_data : mailbox_schemas.MailboxBase ):
    print('create_my_mailbox 작동')

    # 쿼리문으로 데이터 베이스 조회(User, MailBoxPosition)
    owner_q = db.query(User).filter(User.id == mailbox_data.owner_id)
    mailbox_position_q = db.query(MailBoxPosition).filter(MailBoxPosition.id == mailbox_data.mailbox_position_id)
    
    try:
        owner_id = owner_q.exists()
        mailbox_position_id = mailbox_position_q.exists()
    except NoResultFound:
        raise KeyError
    
    # 주소는 uuid4 사용.
    address = str(uuid.uuid4())

    # 편지함 이름
    if mailbox_data.name == "":
        name = owner_q.username
    else:
        name = mailbox_data.name
    
    new_mailbox = MailBox(
        owner_id = owner_id,
        mailbox_position_id = mailbox_position_id,
        address = address
        name = name
    )
    db.add(new_mailbox)
    db.commit()
    db.refresh(new_mailbox)

    return print('ok')
    


