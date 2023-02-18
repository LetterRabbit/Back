from sqlalchemy import *
from sqlalchemy.orm import *
from core.database import Base


class MailBox(Base):
    __tablename__ = "mailboxes"
        
    id                  = Column(Integer, primary_key=True, index=True, autoincrement=True)
    owner_id            = Column(Integer, ForeignKey("users2.id"))
    mailbox_position_id = Column(Integer, ForeignKey("mailbox_positions.id"), nullable = True)
    address             = Column(String(200), nullable = False)
    created_at          = Column(DateTime, default=func.utc_timestamp())
    updated_at          = Column(DateTime, default=func.utc_timestamp(), onupdate=func.utc_timestamp())
    
    owner       = relationship("User2", back_populates = 'my_mailbox')
    position    = relationship("MailBoxPosition", back_populates = 'target_box')

class MailBoxPosition(Base):
    __tablename__ = "mailbox_positions"
    id   = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(200), nullable = False)

    target_box  = relationship("MailBox", back_populates = "position")
    
class User2(Base):
    __tablename__ = "users2"
        
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
    my_mailbox = relationship("MailBox", back_populates = 'owner')

