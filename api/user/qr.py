import pyqrcode
import boto3
import os, uuid
from botocore.exceptions import ClientError
from pathlib import Path

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")

# AWS S3 버킷 이름
S3_BUCKET_NAME = 'letterforyou'

# boto3 S3 클라이언트 생성
s3_client = boto3.client('s3',
                         region_name="ap-northeast-2",
                         aws_access_key_id = AWS_ACCESS_KEY,
                         aws_secret_access_key = AWS_SECRET_KEY
                         )

def generate_qrcode(url:str, id):
    qrcode = pyqrcode.create(url)
    img = qrcode.png(f'./api/user/image/{id}.png',scale=4)
    return img

def save_aws_s3(url, id):
    try:
        generate_qrcode(url, id)
        cwd = Path.cwd()
        with open(f'{cwd}/api/user/image/{id}.png', 'rb') as f:
            s3_client.upload_fileobj(f, S3_BUCKET_NAME, f"qr_images/{id}.png")
        s3_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/qr_images/{id}.png"
        os.remove(f"{os.getcwd()}/api/user/image/{id}.png")
        return s3_url
    
    except Exception as e:
        os.remove(f"{os.getcwd()}/api/user/image/{id}.png")
        return {'message': f'Failed to upload image to S3\n{e}'}