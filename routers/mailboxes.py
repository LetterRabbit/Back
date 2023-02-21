from fastapi import APIRouter, Request, Response, Header, Depends, status
from sqlalchemy.orm import Session
from api.mailbox.mailbox import create_my_mailbox
from typing import Optional
from core import database
from schemas.mailbox_schemas import MailboxBase
router = APIRouter(
    prefix="/mailbox",
    tags=["mailbox"],
)

@router.get("/check")
async def CheckGet():
    print('mailbox activate')
    return {"message" : "mailbox activate"}

@router.post("/create", status_code= status.HTTP_201_CREATED)
async def CreateMailbox(
    db : Session = Depends(database.get_db), data : MailboxBase = Request.body):
    
    mailbox_data = MailboxBase(
        owner_id = data.owner_id,
        mailbox_position_id = data.mailbox_position_id,
        name = data.name
    )
    create_my_mailbox(db = db, mailbox_data = mailbox_data)
    
    return {"message" : "new mailbox created"}