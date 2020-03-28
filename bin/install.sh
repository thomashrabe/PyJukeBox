#!/bin/bash

sudo apt install python3-pip
sudo apt install evtest
sudo pip3 install evdev
sudo pip3 install python-vlc

mkdir -p /home/pi/.jukebox
touch /home/pi/.jukebox/db.jdbd

echo 'Edit crontab and add '
echo '@reboot /home/pi/jukebox/bin/jukebox.sh > /home/pi/.jukebox/jukebox.log 2> /home/pi/.jukebox/jukebox.err'


