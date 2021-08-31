"""
Launch Minecraft server where the world changes every 24 hours.
Assumes that each folder contains a `server.jar` file that corresponds
to each of their versions.

See the .README/ folder for the expected structure for each folder.

To install required dependencies: `pip install schedule mcrcon`.
"""

import time
import os
import json
import schedule
from mcrcon import MCRcon

NO_GUI = True
LAUNCH_ARGS = ("-Xms2G -Xmx16G -XX:+UseG1GC -jar server.jar"
               f" {'nogui' if NO_GUI else ''}")

START_TIME = time.time()

HOST = os.environ["MC_HOST_ADDRESS"]
RCON_PASSWORD = os.environ["MC_RCON_PASSWORD"]
RCON_PORT = int(os.environ["MC_RCON_PORT"])

YELLOW = "#FAA61A"
RED = "#F04747"

# Assumes server folder name starts with "NWSC"
dirs = sorted(x for x in os.listdir() if os.path.isdir(x) and x.startswith("NWSC"))

def select_version():
    """Display a menu to select the version to host first."""
    selection = 0
    max_value = len(dirs)
    
    while True:
        print("Select NWSC version:")
        for i, version in enumerate(dirs):
            print(f"[{i+1}]    {version}")
        selection = int(input("Version: "))
        
        if 1 <= selection <= max_value:
            for i in range(selection-1):
                get_next_server()
            return

        print("Invalid selection")


def get_next_server():
    """Return the folder name and cycle it to the back."""
    x = dirs.pop(0)
    dirs.append(x)
    return x


def start_server():
    """Open a new terminal window and start the server."""
    f = get_next_server()
    cmd = (f"screen -S mc_server -dm bash -c"
           f" \"cd '{os.path.abspath(f)}';"
           f" java {LAUNCH_ARGS}\"")
    
    print()
    print("> " + cmd)
    
    print()
    print(f"Starting {f}...")
    print(f"Next up: {dirs[0]}")
    os.system(cmd)


def send_command(cmd):
    with MCRcon(HOST, RCON_PASSWORD, RCON_PORT) as mc:
        print("[CONSOLE] " + mc.command(cmd))


def warn_server(color, time):
    """Send a message to warn players that the server is restarting."""
    tellraw_arg = ["", {"text": "⚠ ", "color": color},
                   {"text": "Warning    ", "bold": True, "color": color},
                   {"text": f"The server will restart in {time}.", "color": color}]

    send_command("tellraw @a " + json.dumps(tellraw_arg))
    print(f"Sent a warning that the server will restart in {time}.")


def stop_and_start_server():
    send_command("kick @a The server is restarting. Service will resume momentarily.")
    send_command("stop")
    print("Sent a request to stop the server. Will relanch in 60 seconds.")
    time.sleep(60)
    start_server()


schedule.every().day.at("01:00").do(warn_server, YELLOW, "an hour")
schedule.every().day.at("01:30").do(warn_server, YELLOW, "30 minutes")
schedule.every().day.at("01:45").do(warn_server, RED, "15 minutes")
schedule.every().day.at("01:55").do(warn_server, RED, "5 minutes")
schedule.every().day.at("01:59").do(warn_server, RED, "60 seconds")
schedule.every().day.at("02:00").do(warn_server, RED, "10 seconds")
schedule.every().day.at("02:01").do(stop_and_start_server)


if __name__ == "__main__":
    select_version()
    start_server()
    while True:
        schedule.run_pending()
        time.sleep(5)
