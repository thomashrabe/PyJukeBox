# JukeBox

## Setup

sudo apt install vim
sudo apt install ipython
sudo apt install ipython3
sudo apt install python3-pip
sudo apt install evtest
sudo pip3 install evdev

## How to determine device path for USB RFID reader

Run `evtest` and `lsusb`. If no other input is plugged into the computer, `evtest` will output the device path for RFID.
