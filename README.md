# archive-tools
Tools for server archival and hosting archived servers

## Requirements

* Python 3.6+ (tested on 3.9)
* Install pip and screen, if you don't already have them
  ```
  sudo apt-get install screen pip
  ```
* Using `pip`, install mcrcon and schedule
  ```
  pip install mcrcon schedule
  ```
* Set the environment variables for the RCON password, port, and the server address.
  
  Since this is designed to be run on the server, the address can be the private IPv4 address.
  ```bash
  export MC_RCON_PASSWORD=password123
  export MC_RCON_PORT=1234
  export MC_HOST_ADDRESS=0.0.0.0
  ```
* Scripts should be run on the hosting server.

## Usage

### set-gamerules.py

Used to modify the world gamerules to ensure that the world can be spectated and preserved in its original form.

Simply run the file from the terminal using `python set-gamerules.py` and follow the on-screen prompts.


### start-tour.py

Used to cycle the maps each day. Make sure that each world folder name starts with "NWSC" and contains the server.jar
file in the immediate folder.

Simply run the file from the terminal using `python start-tour.py` and follow the on-screen prompts.
