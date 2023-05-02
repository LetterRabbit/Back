#!/bin/bash

FILENAME="start_dev.sh.enc"

echo "Enter password:"
read -s PASSWORD

openssl aes-256-cbc -d -in start_dev.sh.enc -pass pass:$PASSWORD | bash