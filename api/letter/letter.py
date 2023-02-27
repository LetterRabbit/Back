import requests, json, os, random
from fastapi import Depends, HTTPException, status
from models.models  import MailBox
from schemas import letter_schemas
from sqlalchemy.orm import Session
from models.models import User, MailBoxPosition, Letter, MailBox

from sqlalchemy.orm.exc import NoResultFound

def find_mailbox(db: Session, target_address):
    try:
        mailbox_id = db.query(MailBox.id).filter(MailBox.address == target_address).first()[0]
        return mailbox_id
    except:
        raise KeyError

def generate_random_writer_name(name):
    if not name == "":
        return name
    
    else:
        mbti_list = ['INTJ', 'INTP', 'ENTJ', 'ENTP', 'INFJ', 'INFP', "ENFJ", 'ENFP', 'ISTJ', 'ISFJ', 'ESTJ', 'ESFJ', 'ISTP', 'ISFP', 'ESTP', 'ESFP' ]
        animal_list = ['호랑이', '곰돌이', '원숭이', '햄스터']

        random_mbti = random.choice(mbti_list)
        random_animal = random.choice(animal_list)

        random_writer_name = random_mbti + " " + random_animal

        return random_writer_name


def write_my_letter(db : Session, letter_data : letter_schemas.WriteLetter ):
    # 메일박스 uuid 주소(address)로 id값 찾기
    mailbox_id = find_mailbox(db = db, target_address = letter_data.address)
    # 랜덤 편지 작성자명 생성 (input 값이 None 이면 작동)
    username = generate_random_writer_name(name = letter_data.username)
    
    new_letter = Letter(
        mailbox_id = mailbox_id,
        username = username,
        description = letter_data.description
    )

    db.add(new_letter)
    db.commit()
    db.refresh(new_letter)
