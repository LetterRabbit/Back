from fastapi import APIRouter, Request, Response, Header, Depends, status, Query
from sqlalchemy.orm import Session
from api.letter.letter import write_my_letter
from typing import Optional
from core import database
from schemas.letter_schemas import RequestLetter, WriteLetter
router = APIRouter(
    prefix="/letter",
    tags=["letter"],
)

@router.get("/check")
async def CheckGet():
    print('letter activate')
    return {"message" : "letter activate"}

@router.post("/write/", status_code= status.HTTP_201_CREATED)
async def CreateMailbox(
    address : str = Query(None, title='mailbox_address(uuid)', description= '쿼리 스트링으로 메일박스 uuid 값이 필요합니다.'),
    db : Session = Depends(database.get_db), 
    data : RequestLetter = Request.body):
    
    letter_data = WriteLetter(
        address= address,
        username = data.username,
        description = data.description
    )
    
    write_my_letter(db= db, letter_data= letter_data)
    
    return {"message" : "new mailbox created"}