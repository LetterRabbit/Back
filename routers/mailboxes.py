from fastapi                import APIRouter, Request, Response, Header, Depends, status
from sqlalchemy.orm         import Session
from api.mailbox.mailbox    import create_my_mailbox, open_my_mailbox, open_my_letter
from core.decoration        import get_user_from_jwt
from core                   import database
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

@router.get("/open", status_code= status.HTTP_200_OK)
async def OpenMailbox(request : Request, db : Session = Depends(database.get_db)):
    access_token = request.headers.get('access_token')
    user_data = get_user_from_jwt(access_token= access_token, db= db)
    letters = open_my_mailbox(db = db, data = user_data)
    
    return {"message" : letters}

@router.get("/open/{letter_id}", status_code= status.HTTP_200_OK)
async def OpenLetter(request : Request, letter_id : int, db : Session = Depends(database.get_db)):
    access_token = request.headers.get('access_token')
    user_data = get_user_from_jwt(access_token= access_token, db= db)
    letter = open_my_letter(db=db, data= user_data, letter_id= letter_id)
    
    return {"message" : letter}
