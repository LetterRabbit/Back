from pydantic import BaseModel
from typing import List, Optional

class MailboxBase(BaseModel): 
    owner_id : int
    mailbox_position_id : int
    

class MailboxCreate(MailboxBase):
    address : str

