from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

class MailboxBase(BaseModel): 
    owner_id : int
    mailbox_position_id : int
    name : str
    

class MailboxCreate(MailboxBase):
    address : str

class PostCreateMailbox(BaseModel):
    mailbox_position_id : int
    name : str
    class Config:
        json_encoders = {ObjectId: str}

