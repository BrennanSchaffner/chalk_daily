#!/bin/sh 

# Author : Brennan

cd /home/pi

echo "this may take a few minute"

sudo apt update
sudo apt install git

git clone https://github.com/BrennanSchaffner/chalk_daily.git

sudo apt install git

pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
