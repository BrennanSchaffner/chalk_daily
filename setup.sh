#!/bin/sh 

# Author : Brennan

cd /home/pi

echo "this may take a few minute"

sudo apt update
sudo apt install git

git clone https://github.com/BrennanSchaffner/chalk_daily.git

cd ./chalk_daily
git pull

pip install easygui
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

FILE=/home/pi/credentials.json
if [ -f "$FILE" ]; then
    echo "$FILE exists."
else 
    echo "$FILE does not exist."
    xdg-open https://developers.google.com/sheets/api/quickstart/go
fi




