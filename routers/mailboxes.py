from fastapi                    import APIRouter, Request, Response, Body, Depends, status
from sqlalchemy.orm             import Session
from api.mailbox.mailbox        import create_my_mailbox, open_my_mailbox, open_my_letter
from core.decoration            import get_user_from_jwt
from core                       import database
from schemas.mailbox_schemas    import PostCreateMailbox, MailboxBase
from fastapi.responses          import JSONResponse
from bson                       import ObjectId
from fastapi.encoders           import jsonable_encoder
router = APIRouter(
    prefix="/mailbox",
    tags=["mailbox"],
)

@router.get("/check")
async def CheckGet():
    print('mailbox activate')
    return JSONResponse(content="mailbox activate", status_code=200)

@router.post("/create")
async def create_mailbox(request: Request, db: Session = Depends(database.get_db),data: PostCreateMailbox = Body(...),):

    token = request.cookies.get('access_token')  
    user_info = get_user_from_jwt(token, db=db)
    mailbox_data = MailboxBase(
        owner_id = user_info.id,
        mailbox_position_id = data.mailbox_position_id,
        name = data.name
    )
    create_my_mailbox(db=db, mailbox_data=mailbox_data)

    return JSONResponse(content="Create mail box", status_code=201)

@router.get("/open")
async def OpenMailbox(request: Request, db: Session = Depends(database.get_db)):
    access_token = request.cookies.get('access_token')
    user_data = get_user_from_jwt(access_token=access_token, db=db)
    all_letters = open_my_mailbox(db=db, data=user_data)

    return JSONResponse(content= all_letters, status_code=200)

@router.get("/open/{letter_id}")
async def OpenLetter(request : Request, letter_id : int, db : Session = Depends(database.get_db)):
    access_token = request.cookies.get('access_token')
    user_data = get_user_from_jwt(access_token= access_token, db= db)
    letter = open_my_letter(db=db, data= user_data, letter_id= letter_id)

    return JSONResponse(content= dict(letter), status_code=200)