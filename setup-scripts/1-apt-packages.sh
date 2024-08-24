#!/bin/bash

sudo apt update
sudo apt install screen openjdk-21-jre firewalld pip zip unzip

# Get Python 3.10 for other scripts
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.10-full

echo Checking to see if everything\'s installed...

screen --version
java --version
pip --version
firewalld

pip install mcrcon schedule
