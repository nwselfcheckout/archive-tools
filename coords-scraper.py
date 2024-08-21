import os
import re
import gzip
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass

last_log_file = None


@dataclass
class CoordinateEntry:
    x: int | None
    y: int | None
    z: int | None
    comment: str


@dataclass
class PlayerMessage:
    time: str
    username: str
    content: str


def parse_log_entry(raw_entry: str) -> PlayerMessage:
    res = re.match(
        r"\[(?P<time>\d\d:\d\d:\d\d)\] \[.+INFO\]: <(?P<username>.+)> (?P<content>.+)",
        raw_entry,
    )
    return PlayerMessage(**res.groupdict()) if res else None


def parse_coordinates(message: str):
    res = re.search(r"(-?\d+)[, ;]+(-?\d+)[, ;]*(-?\d+)?", message)

    if res is None:
        return None

    first, second, third = (int(i) if i else None for i in res.groups())
    if third is None:
        x, y, z = first, None, second
    else:
        x, y, z = first, second, third

    start, end = res.span()
    if start == 0:
        comment = message[end:]
    else:
        comment = message[:start]
    comment = comment.strip()

    return CoordinateEntry(x, y, z, comment)


def scrape_all(log_folder: Path):
    log_files = [
        Path(log_folder).joinpath(f)
        for f in os.listdir(log_folder)
        if f.endswith(".log.gz")
    ]

    for log_file in log_files:
        if not log_file.is_file:
            continue
        with gzip.open(log_file, "r") as f:
            # Boldly assume log file name is in the format: YYYY-MM-DD-n.log.gz
            dt = datetime(*(int(i) for i in log_file.name.split("-")[:3]))

            for line in f.read().decode().splitlines():
                entry = parse_log_entry(line)
                if entry:
                    coords = parse_coordinates(entry.content)
                    if coords:
                        print(entry.content)
                        print(coords)


if __name__ == "__main__":
    scrape_all("logs")
