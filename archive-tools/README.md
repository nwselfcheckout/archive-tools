# archive-tools
Tools for server archival and hosting archived servers

## Requirements

* Python 3.9 (probably works for 3.7+).

* Install pip and screen, if you don't already have them.

  ```
  sudo apt-get install screen pip
  ```
* Using `pip`, install mcrcon and schedule.
  ```
  pip install mcrcon schedule
  ```
* Set the environment variables for the RCON password, port~~, and the server address~~.
  
  Since this is designed to be run on the hosting computer, `localhost` should just work.

  ```bash
  export MC_RCON_PASSWORD=password123
  export MC_RCON_PORT=1234
  ```
* Scripts should be run on the hosting server.

## Usage

### Expected structure

```
NWSC 1/
├─ logs/
├─ eula.txt
├─ server.properties
├─ server.jar
├─ …
NWSC 2/
├─ logs/
├─ eula.txt
├─ server.properties
├─ server.jar
├─ …
NWSC n/
├─ etc…
set-gamerules.py
start-tour.py
```

### set-gamerules.py

Used to modify the world gamerules to ensure that the world can be spectated and preserved in its original form.

Simply run the file from the terminal using `python set-gamerules.py` and follow the on-screen prompts.


### start-tour.py

Used to cycle the maps each day. Make sure that each world folder name starts with "NWSC" and contains the server.jar
file in the immediate folder.

The map order is alphabetical based on the name of each server folder. Enumerating it like the 
[example above](https://github.com/nwselfcheckout/archive-tools#expected-structure) will ensure that it is in the correct order.

Adjust the [launch args](https://github.com/nwselfcheckout/archive-tools/blob/main/start-tour.py#L17-L19) in the script accordingly to accomodate the hosting computer.
```py
NO_GUI = True
LAUNCH_ARGS = ("-Xms2G -Xmx16G -XX:+UseG1GC -jar server.jar"
               f" {'nogui' if NO_GUI else ''}")
```

Simply run the file from the terminal using `python start-tour.py` and follow the on-screen prompts.
