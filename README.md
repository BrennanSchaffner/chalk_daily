### Chalk Daily
## by Brennan Schaffner

# Set-up - TODO: update this

install git on pi 
*'sudo apt update'
*'sudo apt install git'

open terminal and clone this repo by: (make sure you are in home/pi with 'pwd' before)
*'git clone https://github.com/BrennanSchaffner/chalk_daily.git'



install python and pip if you dont have it
*'sudo apt install git'

pip install stuff (maybe)

https://developers.google.com/sheets/api/quickstart/python
might have to enable the api and get credentials and install package^

* move chalk_daily.desktop to desktop
* fix its paths if necessary
* chmod+x path/main.py
* (make desktop icon: https://www.hackster.io/kamal-khan/desktop-shortcut-for-python-script-on-raspberry-pi-fd1c63)

Connect to the internet. 
You need a google account. 

in terminal:
*make sure you are in home/pi with 'pwd'
*sh ./chalk_daily/setup.sh
* At one point, you will be asked to enable the google sheets api. 
** follow the steps
** download credentials.json and move it into /home/pi/ using file explorer
	(If you put it in the git repository, it may get overwritten upon updates)
