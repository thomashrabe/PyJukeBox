#!/bin/bash

# Based on 
# https://linuxhint.com/install_docker_raspberry_pi-2/

curl -fsSL https://get.docker.com -o get-docker.sh
sudo bash get-docker.sh 
sudo usermod -aG docker $(whoami)
echo ''
echo ''
echo 'PI needs a reboot now!'

