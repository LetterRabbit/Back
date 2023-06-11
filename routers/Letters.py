from fastapi import APIRouter, Request, Response, Body, Depends, status, Query
from sqlalchemy.orm import Session
from api.letter.letter import write_my_letter
from typing import Optional
from core import database
from schemas.letter_schemas import RequestLetter, WriteLetter
from models.models import MailBox, User
router = APIRouter(
    prefix="/letter",
    tags=["letter"],
)

@router.get("/check")
async def CheckGet2():
    print('letter activate')
    return {"message" : "letter activate"}

@router.get("/write", status_code= status.HTTP_201_CREATED)
async def CreateMailbox(
    address : str = Query(None, title='mailbox_address(uuid)', description= 'The UUID value for the mailbox is required as a query string.'),
    db : Session = Depends(database.get_db), 
):
    res = db.query(MailBox).filter(MailBox.address == address).first()
    target_user = db.query(User).filter(User.id == res.owner_id).first()

    
    return Response(content=target_user.username)


@router.post("/write", status_code= status.HTTP_201_CREATED)
async def CreateMailbox(
    address : str = Query(None, title='mailbox_address(uuid)', description= 'The UUID value for the mailbox is required as a query string.'),
    db : Session = Depends(database.get_db), 
    data : RequestLetter = Body()):
    
    letter_data = WriteLetter(
        address= address,
        username = data.username,
        description = data.description
    )
    
    write_my_letter(db= db, letter_data= letter_data)
    
    return {"message" : "new letter created"}