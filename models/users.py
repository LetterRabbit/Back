from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from core.database import Base
from sqlalchemy.orm import *
from models.mailbox import *

class User(Base):
    __tablename__ = "users"
        
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(120), unique=True,nullable = False)
    email = Column(String(255), unique=True, nullable = False)
    gender = Column(String(255))
    age_range = Column(String(255))
    birthday = Column(String(255))
    is_activate = Column(Boolean, default = True)
    created_at = Column(DateTime, default=func.utc_timestamp())
    updated_at = Column(DateTime, default=func.utc_timestamp(), onupdate=func.utc_timestamp())
    # 편지함과 1:1 관계 설정값
    # mailbox = relationship("mailbox.MailBox", back_populates = 'mailboxes')