# archive-tools
Tools for server archival and hosting archived servers

## Requirements

* Python 3.6+ (tested on 3.9)
* [`pip install mcrcon`](https://pypi.org/project/mcrcon/)
* Scripts should be run on the hosting server.

## Usage

### set-gamerules.py

Used to modify the world gamerules to ensure that the world can be spectated and preserved in its original form.

Simply run the file from the terminal using `python set-gamerules.py` and follow the on-screen prompts.

### start-tour.py

Used to cycle the maps each day. Make sure that each world folder name starts with "NWSC" and contains the server.jar
file in the immediate folder.

Simply run the file from the terminal using `python start-tour.py` and follow the on-screen prompts.
