import os
import sys
import time

from discord import Embed, SyncWebhook

from coords_scraper import CoordinateEntry, check_logs

POLLING_INTERVAL = 30
WEBHOOK_URL = os.environ['WEBHOOK_URL']


def coord_embed(entry: CoordinateEntry) -> Embed:
    embed = Embed()
    embed.title = entry.comment[:256] if entry.comment else "*No label*"
    embed.add_field(name="X", value=f"```{'-' if entry.x is None else entry.x}```", inline=True)
    embed.add_field(name="Y", value=f"```{'-' if entry.y is None else entry.y}```", inline=True)
    embed.add_field(name="Z", value=f"```{'-' if entry.z is None else entry.z}```", inline=True)
    embed.set_footer(text=entry.username)
    embed.timestamp = entry.dt
    return embed


def send_coords(log_folder: str):
    coords = check_logs(log_folder)
    webhook = SyncWebhook.from_url(WEBHOOK_URL)
    for coord in coords:
        embed = coord_embed(coord)
        webhook.send(embed=embed)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("No log folder provided.")

    while True:
        time.sleep(POLLING_INTERVAL)
        send_coords(sys.argv[1])
