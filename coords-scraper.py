import os
import re
import gzip
import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass


@dataclass
class LastRead:
    log_file: str
    line_number: int

    @classmethod
    def load(cls):
        """Load the last read log file and line number from a JSON file."""
        try:
            with open("last_read.json", "r") as f:
                data = json.load(f)
                return cls(**data)
        except FileNotFoundError:
            return None

    def write(self):
        """Save the current state to a JSON file."""
        with open("last_read.json", "w") as f:
            json.dump(self.__dict__, f)

    def update(self, log_file: str = None, line_number: int = None):
        """Update the log file and line number, and save the state."""
        self.log_file = log_file or self.log_file
        self.line_number = line_number or self.line_number
        self.write()


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


def read_from_logfile(log_file: Path):
    """Read from a SAVED log file, ending with .log.gz."""
    with gzip.open(log_file, "r") as f:
        # Boldly assume log file name is in the format: YYYY-MM-DD-n.log.gz
        dt = datetime(*(int(i) for i in log_file.name.split("-")[:3]))
        parse_log_content(f.read().decode())


def read_from_latest(log_folder: Path, last_read: LastRead):
    """Read from latest.log. Also updates the last read line number."""
    with open(Path(log_folder).joinpath("latest.log"), "r") as f:
        content = f.read()
        parse_log_content(content)
        last_read.update(line_number=str(len(content.splitlines())))


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
        read_from_logfile(log_file)

    # Then, parse the current log file.
    last_read = LastRead(log_files[-1].name, 0)
    read_from_latest(log_folder, last_read)


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

    last_read = LastRead.load()

    if last_read is None:
        # Nothing is read, this is the first run.
        scrape_all(log_folder)

    print(last_read)
    print(log_files)


if __name__ == "__main__":
    # scrape_all("logs")
    poll_logs("logs")
