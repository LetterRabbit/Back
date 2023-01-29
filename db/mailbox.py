from sqlalchemy import *
from sqlalchemy.orm import *
from core.database import Base
from db.users import User

class MailBox(Base):
    __tablename__ = "mailboxes"
        
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user = relationship(User, back_populates = 'mailboxes')
    user_id = Column(Integer, ForeignKey("users.id"))
    mailbox_position = relationship("MailBoxPosition", back_populates = 'mailboxes')
    mailbox_position_id = Column(Integer, ForeignKey("mailbox_positions.id"))
    address = Column(String(200), nullable = False)
    created_at = Column(DateTime, default=func.utc_timestamp())
    updated_at = Column(DateTime, default=func.utc_timestamp(), onupdate=func.utc_timestamp())

class MailBoxPosition(Base):
    __tablename__ = "mailbox_positions"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(200), nullable = False)

