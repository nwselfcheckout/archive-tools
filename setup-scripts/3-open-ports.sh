#!/bin/bash

usage () {
	echo "usage: $0 [port ...]"
	echo "    Open the provided PORTs for TCP and UDP traffic."
	echo "    Typically one for the game (query) server and one for RCON requests."
	exit
}

if [ $# == 0 ]; then
	usage
fi

for port in "$@"
do
	echo "Opening port $port for TCP traffic";
	sudo firewall-cmd --permanent --zone=public --add-port=$port/tcp;
	echo "Opening port $port for UDP traffic";
	sudo firewall-cmd --permanent --zone=public --add-port=$port/udp;
done

echo
echo "Reloading firewall to apply changes..."
sudo firewall-cmd --reload

echo
echo "All done!"
