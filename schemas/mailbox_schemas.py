from pydantic import BaseModel
from typing import List, Optional

class MailboxBase(BaseModel): 
    owner_id : int
    mailbox_position_id : int
    name : str
    

class MailboxCreate(MailboxBase):
    address : str

class CreateMailbox(BaseModel):
    mailbox_position_id : int
    name : str
