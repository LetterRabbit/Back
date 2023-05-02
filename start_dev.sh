#!/bin/bash

echo 1. 파일목록 보여주기
ls

echo  2. python venv 설치
python3 -m venv venv

echo 3. venv 실행
source venv/bin/activate

echo  4. venv 실행 확인
python --version

echo  4. requirements.txt 설치
pip install -r requirements.txt

echo  5. .env 파일생성
touch .env

echo 6. 내용작성

echo   6-1. SECRET_KEY 작성
cd Back
SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
cd ..
echo  6-2. DEBUG 작성
DEBUG='False'

echo 6-3. KAKAO SECRETKEY 작성
KAKAO_REST_API_KEY = "bf304943800c49b11b10998c5f034b8a"

echo 6-4. AWS S3연결을위한 KEY 작성
AWS_ACCESS_KEY = 'AKIAXLJQSSWTA3Y2HAGY'
AWS_SECRET_KEY = '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'


echo 7. DB 정보 입력
echo "Enter DB_USERNAME:"
read -p "DB_USERNAME: " DB_USERNAME
echo "Enter DB_PASSWORD:"
read -p "DB_PASSWORD: " DB_PASSWORD
echo "Enter DB_HOST:"
read -p "DB_HOST: " DB_HOST
echo "Enter DB_PORT:"
read -p "DB_PORT: " DB_PORT
echo "Enter DB_DATABASE:"
read -p "DB_DATABASE: " DB_DATABASE

echo 7. .env 파일 내부에 위에 정의 한 키 작성
echo "SECRET_KEY=\"$SECRET_KEY\"" >> .env
echo "ALGORITHM=\"$ALGORITHM\"" >> .env
echo "ACCESS_TOKEN_EXPIRE_MINUTES=\"$ACCESS_TOKEN_EXPIRE_MINUTES\"" >> .env
echo "KAKAO_REST_API_KEY=\"$KAKAO_REST_API_KEY\"" >> .env
echo "AWS_ACCESS_KEY=\"$AWS_ACCESS_KEY\"" >> .env
echo "AWS_SECRET_KEY"\"$AWS_SECRET_KEY\" >> .env
echo "DEBUG=\"$DEBUG\"" >> .env
echo "DB_USERNAME=\"$DB_USERNAME\"" >> .env
echo "DB_PASSWORD=\"$DB_PASSWORD\"" >> .env
echo "DB_HOST=\"$DB_HOST\"" >> .env
echo "DB_PORT=\"$DB_PORT\"" >> .env
echo "DB_DATABASE=\"$DB_DATABASE\"" >> .env


deactivate
echo 사전작업이 완료 되었습니다.



