# Back
실행방법 (shell script 제작중)


사전준비

mysql
1. mysql -u root -p < 계정접속
2. CREATE DATABASE letter

code
1. Git clone
2. rm -rf venv
3. python3 -m venv venv
4. source venv/bin/activate
5. pip install requirement(s).txt
6. .env 파일생성
(내용)
<pre>
DB_USERNAME = "DB User"
DB_PASSWORD = "DB password"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_DATABASE = "DB name"
</pre>

7. python main.py



make_secret.sh 사용방법
- hex64에 따른 secret_key를 생성해줌

1. 사용 권한설정 (linux 기준 chmod 755 (파일명))
2. 실행 (./make_secret.sh)

pip install 안될시 
1.  python.exe -m pip install --upgrade pip 실행


#### start_dev.sh 사용

1. start_dev.sh.enc 복호화 (가상환경 및 env파일, 필요 python 패키지 설치를 위한 작업)
    2-1. decrypt.sh를 통한 복호화 진행

        - chmod 755 decrypt.sh
        - source decrypt.sh


    2-2. 권한 부여

        - chmod 755 start_dev.sh

    2-3. start_dev.sh 실행

        - source start_dev.sh