from fastapi                    import APIRouter, Request, Response, Body, Depends, status, Header, Query
from sqlalchemy.orm             import Session
from api.mailbox.mailbox        import create_my_mailbox, open_my_mailbox, open_my_letter
from core.decoration            import get_user_from_jwt
from core                       import database
from schemas.mailbox_schemas    import PostCreateMailbox, MailboxBase
from fastapi.responses          import JSONResponse
from fastapi.encoders           import jsonable_encoder
from typing                     import Optional

from models.models import MailBox, Letter

router = APIRouter(
    prefix="/mailbox",
    tags=["mailbox"],
)

@router.get("/check")
async def CheckGet():
    print('mailbox activate')
    return JSONResponse(content="mailbox activate", status_code=200)

@router.post("/create")
async def create_mailbox(
        request: Request, 
        db: Session = Depends(database.get_db),
        data: PostCreateMailbox = Body(...),
        access : Optional[str] = Header(None) 
        ):

    user_info = get_user_from_jwt(access_token = access, db=db)
    mailbox_data = MailboxBase(
        owner_id = user_info.id,
        mailbox_position_id = data.mailbox_position_id,
        name = data.name
    )
    create_my_mailbox(db=db, mailbox_data=mailbox_data)

    return JSONResponse(content="Create mail box", status_code=201)

@router.get("/open")
async def OpenMailbox(
        request: Request, 
        db : Session = Depends(database.get_db),
        access : Optional[str] = Header(None),
        skip : int = Query(0),
        limit : int = Query(5)
        ):
    user_data = get_user_from_jwt(access_token=access, db=db)
    all_letters = open_my_mailbox(db=db, data = user_data, skip = skip, limit = limit )

    return JSONResponse(content= all_letters, status_code=200)

@router.get("/open/{letter_id}")
async def OpenLetter(
        request : Request, 
        letter_id : int, 
        db : Session = Depends(database.get_db),
        access : Optional[str] = Header(None)
        ):
    user_data = get_user_from_jwt(access_token= access, db= db)
    letter = open_my_letter(db=db, data= user_data, letter_id= letter_id)

    return JSONResponse(content= dict(letter), status_code=200)

@router.get("/gen")
async def GenerateMockData(request : Request, db : Session = Depends(database.get_db), access : Optional[str] = Header(None)):
    user_data = get_user_from_jwt(access_token= access, db= db)
    user_id = user_data.id
    mailbox_id = db.query(MailBox.id).filter(MailBox.owner_id == user_id).first()[0]
    
    new_letter = Letter(
        mailbox_id = mailbox_id,
        username = 'test_generate',
        description = '테스트로 생성된 편지입니다.'
    )

    db.add(new_letter)
    db.commit()
    db.refresh(new_letter)
    
    return new_letter

