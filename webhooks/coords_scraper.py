"""
Scrape coordinates sent by players from the log files.

How it works: Latest logs are kept in the `latest.log` file. Minecraft will save
and roll over logs once the day passes or the size of `latest.log` is
sufficiently large.

To poll for changes, we look for entries in the `latest.log` file and keep track
of how far we've read. This is tracked using a JSON file `last_read.json`.

To also scrape any coordinates in older log files or if the logs were rolled
over in between polling cycle, we also keep track of the last log file that was
processed in the same file.
"""

import gzip
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, date, time, timezone
from pathlib import Path


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
    x: int
    y: int | None
    z: int
    comment: str | None
    username: str = None
    dt: datetime = None

    @classmethod
    def from_message(cls, message: str):
        """
        Extract coordinates entry from a text.

        As loosely as possible, tries to look for a pair or triplet of numbers
        separated by commas, space, or semicolons. Returns `None` if not found.
        """
        res = re.search(r"(-?\d+)[, ;]+(-?\d+)[, ;]*(-?\d+)?", message)

        if res is None:
            return None

        first, second, third = (int(i) if i else None for i in res.groups())
        if third is None:
            x, y, z = first, None, second  # no Y-coordinate
        else:
            x, y, z = first, second, third  # all three

        # Look for comments.
        start, end = res.span()
        if start == 0:
            comment = message[end:]
        else:
            comment = message[:start]
        comment = comment.strip() or None

        return cls(x, y, z, comment)


@dataclass
class PlayerMessage:
    time: time
    username: str
    content: str

    @classmethod
    def from_log_entry(cls, log_entry: str):
        """
        Extract a player message from a given log entry.

        Player messages are always an [INFO] event. Allows matching for non-
        vanilla clients (for example, Paper servers marks the record as
        "[Async Chat Thread - #N/INFO]").Returns `None` if the log entry is not
        a player message.
        """
        res = re.match(
            r"\[(?P<time>\d\d:\d\d:\d\d)\] \[.+INFO\]: <(?P<username>.+)> (?P<content>.+)",
            log_entry,
        )
        if res:
            d = res.groupdict()
            return cls(
                time=time.fromisoformat(d["time"]),
                username=d["username"],
                content=d["content"],
            )
        return None


def get_coordinates(log_entries: list[str], log_date: date) -> list[CoordinateEntry]:
    """Extract coordinate entries from log entries."""
    coords = []
    for line in log_entries:
        player_message = PlayerMessage.from_log_entry(line)
        if not player_message:
            continue

        coord = CoordinateEntry.from_message(player_message.content)
        if not coord:
            continue
        coord.dt = datetime.combine(log_date, player_message.time, timezone.utc)
        coord.username = player_message.username
        print(coord)
        coords.append(coord)
    return coords


def read_from_saved(log_file: Path) -> list[CoordinateEntry]:
    """Read from a SAVED log file, ending with .log.gz."""
    with gzip.open(log_file, "r") as f:
        print(f"Reading from {log_file.name}")
        # Boldly assume log file name is in the format: YYYY-MM-DD-n.log.gz
        log_date = date(*(int(i) for i in log_file.name.split("-")[:3]))
        return get_coordinates(f.read().decode().splitlines(), log_date)


def read_from_latest(log_folder: Path, last_read: LastRead) -> list[CoordinateEntry]:
    """Read from the last line read in latest.log."""
    with open(Path(log_folder).joinpath("latest.log"), "r") as f:
        log_entries = f.read().splitlines()
        from_line = last_read.line_number
        last_read.update(line_number=len(log_entries))
        return get_coordinates(log_entries[from_line:], date.today())


def scrape_all(log_folder: Path):
    log_files = sorted(
        Path(log_folder).joinpath(f)
        for f in os.listdir(log_folder)
        if f.endswith(".log.gz")
    )  # God bless ISO-8601.
    coords = []

    # First, parse all of the saved log files.
    for log_file in log_files:
        coords += read_from_saved(log_file)

    # Then, parse the current log file.
    last_read = LastRead(log_files[-1].name, 0)
    coords += read_from_latest(log_folder, last_read)
    return coords


def check_logs(log_folder: str | Path) -> list[CoordinateEntry]:
    """Check the log folders for any new coordinate entries."""
    log_folder = Path(log_folder)
    log_files = sorted(f for f in os.listdir(log_folder) if f.endswith(".log.gz"))
    last_read = LastRead.load()

    # Nothing is read, this is the first run.
    if last_read is None:
        print("First run, scraping everything.")
        return scrape_all(log_folder)

    # Scrape log files that was just created.
    coords = []
    if last_read.log_file != log_files[-1]:
        print("New log file(s) rolled over.")
        new_index = log_files.index(last_read.log_file) + 1
        for log_file in log_files[new_index:]:
            coords += read_from_saved(log_folder / log_file)
        last_read.update(log_file=log_files[-1])

    # Scrape from latest.log.
    coords += read_from_latest(log_folder, last_read)
    print(last_read)
    return coords


if __name__ == "__main__":
    check_logs("logs")
