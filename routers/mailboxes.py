from fastapi import APIRouter, Request, Response, Header, Depends, status
from sqlalchemy.orm import Session
from api.mailbox.mailbox import create_my_mailbox

from models import models
from core import database
from core.decoration import get_user_from_jwt
from schemas.mailbox_schemas import MailboxBase, CreateMailbox

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
    request : Request,
    db : Session = Depends(database.get_db), 
    data : CreateMailbox = Request.body
    ):

    token = request.headers.get('access_token')
    user_info = get_user_from_jwt(token, db=db)
    
    mailbox_data = MailboxBase(
        owner_id = user_info.id,
        mailbox_position_id = data.mailbox_position_id,
        name = data.name
    )
    create_my_mailbox(db = db, mailbox_data = mailbox_data)
    
    return {"message" : "new mailbox created"}