import requests, json, os, uuid
from fastapi import Depends, HTTPException, status
from core.database import get_db
from models.mailbox  import MailBox
from schemas import mailbox_schemas
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from datetime import datetime, timedelta

def create_my_mailbox(db : Session, mailbox_data : mailbox_schemas.MailboxBase ):
    print('create_my_mailbox')
    owner_id = mailbox_data.owner_id
    print(owner_id)
    mailbox_position_id = mailbox_data.mailbox_position_id
    print(mailbox_position_id)
    # 주소는 uuid4 사용.
    address = str(uuid.uuid4())
    
    new_mailbox = MailBox(
        owner_id = owner_id,
        mailbox_position_id = mailbox_position_id,
        address = address
    )
    db.add(new_mailbox)
    db.commit()
    db.refresh(new_mailbox)

    return print('ok')
    


