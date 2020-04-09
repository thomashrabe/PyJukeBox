#!/bin/bash

sudo apt install python3-pip
sudo apt install evtest
sudo pip3 install evdev
sudo pip3 install python-vlc

python3 ./../src/jukebox/jukebox.py --init --db ~/.jukebox/db.jdbd

