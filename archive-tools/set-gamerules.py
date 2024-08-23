"""
Set the gamemodes to prepare the server.

To install required dependencies: `pip install mcrcon`.
"""

import os
from mcrcon import MCRcon


HOST = os.environ["MC_HOST_ADDRESS"]
RCON_PASSWORD = os.environ["MC_RCON_PASSWORD"]
RCON_PORT = int(os.environ["MC_RCON_PORT"])


def send_command(cmd):
    with MCRcon(HOST, RCON_PASSWORD, RCON_PORT) as mc:
        print(cmd)
        return "[CONSOLE] " + mc.command(cmd)


if __name__ == "__main__":
    rules = {
        "keepInventory": "true",
        "doFireTick": "false",
        "doMobGriefing": "false",  # older versions
        "mobGriefing": "false",  # newer alias
        "spectatorsGenerateChunks": "true",
    }

    for rule, value in rules.items():
        send_command(f"gamerule {rule} {value}")

    print()
    input("Game rules set. Hit Enter to verify.")
    print()

    check_results = []
    for rule, value in rules.items():
        msg = send_command(f"gamerule {rule}")
        res = "PASS" if msg.endswith(value) else "FAIL"
        check_results.append(f"[{res}]    {msg}")

    print()
    print("\n".join(check_results))
    print()

    input("All done.")
