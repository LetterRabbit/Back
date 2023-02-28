import pyqrcode
import boto3
from botocore.exceptions import ClientError


# AWS S3 버킷 이름
S3_BUCKET_NAME = 'your-s3-bucket-name'

# boto3 S3 클라이언트 생성
s3_client = boto3.client('s3')


def generate_qrcode(url:str):
    qrcode = pyqrcode.create(url)
    img = qrcode.png("image.png", scale=4)
    return img

def save_aws_s3(image, username):
    try:
        s3_client.put_object(
            Body=image,
            Bucket=S3_BUCKET_NAME,
            Key=f'qr_images/{username}.png'  # 업로드할 파일의 이름
        )
        s3_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/qr_images/{username}.png"
        return s3_url
    
    except ClientError as e:
        print(e)
        return {'message': 'Failed to upload image to S3'}