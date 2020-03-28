# JukeBox

Inspired by toniebox but too cheap to buy one. Too much of a nerd to say I can build myself!
Could not get the installtion for [Pnoniebox](https://www.iphone-ticker.de/wochenend-projekt-kontaktlose-musikbox-fuer-kinder-123063/)
to work so here is the code for a simple version of RFID card enabled MP3 players on a Raspberry Pi.

## Setup
```
sudo apt install vim
sudo apt install ipython3
sudo apt install python3-pip
sudo apt install evtest
sudo pip3 install evdev
sudo pip3 install python-vlc
```

## How to determine device path for USB RFID reader

Run `evtest` and `lsusb`. If no other input is plugged into the computer, `evtest` will output the device path for RFID.

## Setup Media db
Create a JSON file of the format 
```
{
    "RFID_CODE" : "/path/to/a/audio/file.mp3"
}
```
