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
* Set the environment variables for the RCON password and port.

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
[example above](#expected-structure) will ensure that it is in the correct order.

Adjust the [JVM launch args](https://github.com/nwselfcheckout/mc-utils/blob/b1e57fe0117364ea48aa2bfb894694e31a3f8947/archive-tools/start-tour.py#L17)
in the script accordingly to accomodate the hosting computer.
```py
LAUNCH_ARGS = "-Xms2G -Xmx12G -XX:+UseG1GC"
```

> **Note:** These are arguments that will be applied to all saves. Some saves may have additional arguments
> specified in their folder. For more info, see [logj4-patch](https://github.com/nwselfcheckout/mc-utils/tree/main/archive-tools/log4j-patch).

Simply run the file from the terminal using `python start-tour.py` and follow the on-screen prompts.
