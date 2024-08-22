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


def parse_log_content(raw_str: str):
    """Parse content of the log file.

    Assumes the argument is a decoded, newline-terminated string of the log file.
    """
    for line in raw_str.splitlines():
        entry = parse_log_entry(line)
        if entry:
            coords = parse_coordinates(entry.content)
            if coords:
                print(entry.content)
                print(coords)


def scrape_all(log_folder: Path):
    log_files = [
        Path(log_folder).joinpath(f)
        for f in os.listdir(log_folder)
        if f.endswith(".log.gz")
    ]
    log_files.sort()  # God bless ISO-8601.

    # First, parse all of the saved log files.
    for log_file in log_files:
        if not log_file.is_file:
            continue
        with gzip.open(log_file, "r") as f:
            # Boldly assume log file name is in the format: YYYY-MM-DD-n.log.gz
            dt = datetime(*(int(i) for i in log_file.name.split("-")[:3]))
            parse_log_content(f.read().decode())

    # Then, parse the current log file.
    with open(Path(log_folder).joinpath("latest.log"), "r") as f:
        parse_log_content(f.read())


"""
need to keep track of:
- last SAVED log file
- line number read in LATEST.log

in each polling cycle:
- check the highest number of the log files
- if it is different than the last SAVED log file, this means a new log file was created.
    - starting from that file:
        - read and parse coords from the line number
        - update file name
- otherwise:
    - just read from latest.log
    - update line number
"""


def poll_logs(log_folder: str):
    log_files = os.listdir(log_folder)
    log_files.sort()
    log_files = [f for f in log_files if f.endswith(".log.gz")]

    last_log_file = os.getenv("last_log_file")  # The last SAVED log file (.log.gz file)
    last_line_read = os.getenv("last_line_read")

    if last_log_file is None:
        scrape_all(log_folder)
        os.environ["last_log_file"] = log_files[-1]

    print(log_files)


if __name__ == "__main__":
    # scrape_all("logs")
    poll_logs("logs")
