# Chalk Daily
## by Brennan Schaffner

## Set-up 

Connect to the internet. 
You need a google account. 
Make sure Rasbperry Pi has 5V 2A power supply
I dont know the RAM requirements, yet. 

## Just Once
in terminal:
* make sure you are in home/pi with 'pwd' (use 'cd /home/pi' if you are not)
* 'sh ./chalk_daily/setup.sh'
* At one point, you may be asked to enable the google sheets api and sign into google. 
** follow the steps (press Next, select 'Desktop app' and Create)
** Download client configuration. Then move credentials.json from downloads into /home/pi/ using the file explorer
	(If your credentials change for some reason, (maybe you switched google accounts) then delete your old credentials.json and redownload)
** Close the browser window
* Copy the Chalk Daily desktop shortcut to your desktop (or where ever you want it)

## Start it
* Run the Chalk Daily desktop shortcut (may load for a few seconds)
* give it the link to your google sheet formatted like [this](./example_spreadsheet.jpg)

## If you want to update (I will probably tell you if I made changes)
* open terminal
* cd chalk_daily/
* git pull
* I might change this method to be automatic someday via the setup script or something