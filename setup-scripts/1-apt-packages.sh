#!/bin/bash

sudo apt update
sudo apt install screen openjdk-17-jre-headless firewalld pip

echo Checking to see if everything\'s installed...

screen --version
java --version
pip --version
firewalld
