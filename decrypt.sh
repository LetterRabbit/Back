#!/bin/bash

FILENAME="start_dev.sh.enc"

# Download and install OpenSSL version
curl -O https://www.openssl.org/source/openssl-$OPENSSL_VERSION.tar.gz
tar -xvzf openssl-$OPENSSL_VERSION.tar.gz
cd openssl-$OPENSSL_VERSION
./config
make
sudo make install

cd ./Back
echo "Enter the decryption password received from the administrator:"
read -s PASSWORD

openssl aes-256-cbc -d -in start_dev.sh.enc -pass pass:$PASSWORD | bash

rm openssl-$OPENSSL_VERSION.tar.gz
echo "설치 파일 삭제 완료"