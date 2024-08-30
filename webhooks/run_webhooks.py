import os
import sys
import time

from discord import SyncWebhook

from coords_scraper import check_for_coords
from server_status import query_server

POLLING_INTERVAL = int(os.getenv("POLLING_INTERVAL", 30))
COORD_WEBHOOK_URL = os.environ["COORD_WEBHOOK_URL"]
STATUS_WEBHOOK_URL = os.environ["STATUS_WEBHOOK_URL"]

STATUS_MESSAGE_ID = int(os.getenv("STATUS_MESSAGE_ID") or 0)


def send_coords(log_folder: str):
    coords = check_for_coords(log_folder)
    webhook = SyncWebhook.from_url(COORD_WEBHOOK_URL)
    for coord in coords:
        embed = coord.to_embed()
        webhook.send(embed=embed)


def update_server_status(message_id: int):
    server = query_server()
    webhook = SyncWebhook.from_url(STATUS_WEBHOOK_URL)
    embed = server.to_embed()

    # First-time setup.
    if not message_id:
        message = webhook.send(embed=embed, wait=True)
        raise UserWarning(
            f"FIRST-TIME SETUP: The message has been sent with the ID {message.id}. "
            f"Set the environment variable `STATUS_MESSAGE_ID` to this value and re-run this script."
        )

    message = webhook.fetch_message(message_id)
    message.edit(embed=embed)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("No log folder provided.")

    print(f"Polling interval: {POLLING_INTERVAL}")

    while True:
        try:
            send_coords(sys.argv[1])
            update_server_status(STATUS_MESSAGE_ID)

            time.sleep(POLLING_INTERVAL)
        except Exception as e:
            print(f"Something went wrong: {e}")
