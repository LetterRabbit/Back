from fastapi                    import APIRouter, Request, Response, Body, Depends, status, Header, HTTPException, Query
from sqlalchemy.orm             import Session
from sqlalchemy                 import Table, MetaData
from api.mailbox.mailbox        import create_my_mailbox, open_my_mailbox, open_my_letter, get_mailbox_id
from api.user.qr                import save_aws_s3
from core.decoration            import get_user_from_jwt
from core                       import database
from schemas.mailbox_schemas    import PostCreateMailbox, MailboxBase
from fastapi.responses          import JSONResponse
from fastapi.encoders           import jsonable_encoder
from typing                     import Optional
import json
from models.models              import MailBox, Letter
import smtplib
from email.mime.text import MIMEText

router = APIRouter(
    prefix="/mailbox",
    tags=["mailbox"],
)

@router.get("/check")
async def check_get(request: Request):
    client_host = request.client.host
    client_port = request.client.port
    server_port = request.scope.get("server")[1]

    return JSONResponse(content={
        "IP": client_host,
        "client Port": client_port,
        "server Port": server_port
    }, status_code=200)

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

    mailbox_query =  create_my_mailbox(db=db, mailbox_data=mailbox_data)
    
    url = f"https://letter-rabbit-client.vercel.app/mailbox/{mailbox_query.address}"
    url_qr = save_aws_s3(url, user_info.id)
    mytable = Table('users', MetaData(), autoload=True, autoload_with=database.engine)
    qr = mytable.update().where(mytable.c.id == user_info.id).values(self_domain = url, qr_code = url_qr)
    database.engine.execute(qr)

    if mailbox_query:
        return JSONResponse(content=mailbox_query.address, status_code=201)

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
    res = open_my_letter(db=db, data= user_data, letter_id= letter_id)
    
    print(res)
    
    return JSONResponse(content=res, status_code=200)


class LetterForYouEmail:
    def __init__(self):
        self.default_email = 'letter4yous2@gmail.com'
        self.mail_app_pwd  = 'xqagjxmlxpbmlwqe'

    def send_email(self, data):
        self.smtp = smtplib.SMTP('smtp.gmail.com', 587)
        self.smtp.starttls()
        self.smtp.login(self.default_email, self.mail_app_pwd)
        
        data = data
        letter_id = data.id
        letter_desc = data.description
        self.text = f'[신고가 접수된 편지 ID] : {letter_id}\n[편지 내용] : {letter_desc}'

        self.msg = MIMEText(self.text)

        self.smtp.sendmail(self.default_email, self.default_email, self.msg.as_string())
        self.smtp.quit()
    
@router.post("/report/{letter_id}")
def SendReportLetter(letter_id : int, db : Session = Depends(database.get_db), access : Optional[str] = Header(None) ):
    user_data = get_user_from_jwt(access_token = access, db = db)
    user_id = user_data.id
    print(user_id)
    user_mailbox_id = db.query(MailBox.id).filter(MailBox.owner_id == user_id).first()[0]
    print(user_mailbox_id)
    letter_mailbox_id = db.query(Letter.mailbox_id).filter(Letter.id == letter_id).first()[0]
    if user_mailbox_id == letter_mailbox_id:
        report_letter_data = db.query(Letter).filter(Letter.id == letter_id).first()
        letter_email = LetterForYouEmail()
        letter_email.send_email(report_letter_data)
        return JSONResponse(content = "reported", status_code = 200)
    else:
        return JSONResponse(content = "Report failed", status_code = 200)

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

@router.get("/delete/{letter_id}")
async def DeleteLetter(request : Request, letter_id : int, db : Session = Depends(database.get_db), access : Optional[str] = Header(None)):
    user_data = get_user_from_jwt(access_token = access, db = db)
    user_id = user_data.id

    mailbox = db.query(MailBox).filter(MailBox.owner_id == user_id).first()

    if not mailbox:
        raise HTTPException(status_code = 404, detail = "Mailbox does not exist")

    delete_letter = db.query(Letter).filter(Letter.id == letter_id, Letter.mailbox_id == mailbox.id).first()
    
    if delete_letter:
        db.delete(delete_letter)
        db.commit()

        return JSONResponse(content = f"letter_id : {letter_id} has been deleted", status_code = 200)
    else:
        raise HTTPException(status_code = 404, detail = f"letter_id : {letter_id} does not exist")