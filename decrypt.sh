#!/bin/bash

FILENAME="start_dev.sh.enc"

echo "Enter password:"
read -s PASSWORD

openssl enc -d -aes-256-cbc -in $FILENAME -out start_dev.sh -pass pass:$PASSWORD