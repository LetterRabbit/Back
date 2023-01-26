from pydantic import BaseModel
from typing import List, Optional

class UserBase(BaseModel):
    username : str
    email : str
    birthday : str

class UserCreate(UserBase):
    gender : str
    age_range : str