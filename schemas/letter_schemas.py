from pydantic import BaseModel
from typing import List, Optional

class LetterBase(BaseModel): 
    mailbox_id : int
    username : int
    description : str

class WriteLetter(BaseModel):
    address : str
    username : str
    description : str

class RequestLetter(BaseModel):
    username : str
    description : str