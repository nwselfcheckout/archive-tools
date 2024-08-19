#!/bin/bash

sudo apt update
sudo apt install screen openjdk-21-jre firewalld pip

echo Checking to see if everything\'s installed...

screen --version
java --version
pip --version
firewalld
