from sqlalchemy import Boolean, Column, Integer, String,\
    DateTime, ForeignKey, func
from core.database import Base
from sqlalchemy.orm import *


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(120), unique=True,nullable = False)
    email = Column(String(255), unique=True, nullable = False)
    gender = Column(String(255))
    age_range = Column(String(255))
    birthday = Column(String(255))
    is_activate = Column(Boolean, default = True)
    qr_code = Column(String(255), nullable = True)
    self_domain = Column(String(255), nullable = True)
    created_at = Column(DateTime, default=func.utc_timestamp())
    updated_at = Column(DateTime, default=func.utc_timestamp(), onupdate=func.utc_timestamp())

    my_mailbox = relationship("MailBox", back_populates = 'owner')

class MailBox(Base):
    __tablename__ = "mailboxes"
    id                  = Column(Integer, primary_key=True, index=True, autoincrement=True)
    owner_id            = Column(Integer, ForeignKey("users.id"), unique = True)
    mailbox_position_id = Column(Integer, ForeignKey("mailbox_positions.id"), nullable = True)
    address             = Column(String(200), nullable = False)
    name                = Column(String(200), nullable = False)
    created_at          = Column(DateTime, default=func.utc_timestamp())
    updated_at          = Column(DateTime, default=func.utc_timestamp(), onupdate=func.utc_timestamp())

    owner               = relationship("User", back_populates = 'my_mailbox')
    position            = relationship("MailBoxPosition", back_populates = 'target_box')
    from_letters        = relationship("Letter", back_populates = 'to_mailbox')

class MailBoxPosition(Base):
    __tablename__ = "mailbox_positions"
    id   = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(200), nullable = False)

    target_box  = relationship("MailBox", back_populates = "position")

class Letter(Base):
    __tablename__ = "letter"
    id          = Column(Integer, primary_key=True, index=True, autoincrement=True)
    mailbox_id  = Column(Integer, ForeignKey("mailboxes.id"))
    username    = Column(String(200))
    description = Column(String(255))
    deleted_at  = Column(DateTime, default = func.ADDDATE(func.utc_timestamp(), 30))
    created_at  = Column(DateTime, default=func.utc_timestamp())

    to_mailbox = relationship("MailBox", back_populates = 'from_letters')
    