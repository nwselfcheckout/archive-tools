import os
import sys
import time

from discord import SyncWebhook

from coords_scraper import check_for_coords

POLLING_INTERVAL = int(os.getenv("POLLING_INTERVAL", 30))
COORD_WEBHOOK_URL = os.environ["COORD_WEBHOOK_URL"]
STATUS_WEBHOOK_URL = os.environ["STATUS_WEBHOOK_URL"]


def send_coords(log_folder: str):
    coords = check_for_coords(log_folder)
    webhook = SyncWebhook.from_url(COORD_WEBHOOK_URL)
    for coord in coords:
        embed = coord.to_embed()
        webhook.send(embed=embed)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("No log folder provided.")

    print(f"Polling interval: {POLLING_INTERVAL}")

    while True:
        send_coords(sys.argv[1])
        time.sleep(POLLING_INTERVAL)
