# mc-setup-scripts
Scripts for setting up a brand new Minecraft server on a Linux machine (Ubuntu, in this case).

## Before running
If you are cloning the repo, you may need to delegate read/write permission on the files to
run them.

```sh
chmod +xr *
```

## 1-apt-packages.sh
Run to install screen, JRE, firewalld, and pip.

## 2-set-envars.sh
Contains the environment variable names that needs to be configured for other scripts
(like [archive-tools](https://github.com/nwselfcheckout/archive-tools)) to run.

## 3-open-ports.sh
Run to open the necessary ports for traffic. Typically, two ports are open for the query server
and RCON requests. The former is required for users to connect (and for monitoring), while the
latter is primarily used for scheduled restarts.

Check the ports defined in the [server.properties](https://minecraft.fandom.com/wiki/Server.properties)
file to see which ports needs to be opened.

```properties
rcon.port=5678
query.port=1234
server-port=1234
```
To open ports `1234` and `5678`, simply run:

```sh
./3-open-ports.sh 1234 5678
```

> **Note:** The server and query port may share the same number (because one uses TCP and the other uses UDP).
> However, if they are all different, remember to open all of them!

### Check the network's ingress

In addition to opening the ports on the hosting computer, ensure that the network's ingress rules also allow
traffic through the specified ports. At the very least, it must allow traffic for the game port (`server-port`
in server.properties) in order for users to connect.
