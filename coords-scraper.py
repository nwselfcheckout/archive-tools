import os
import re
import gzip
import json
from pathlib import Path
from datetime import datetime, date, time
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
    username: str = None
    dt: datetime = None

    @classmethod
    def from_message(cls, message: str):
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

        return cls(x, y, z, comment)


@dataclass
class PlayerMessage:
    time: time
    username: str
    content: str

    @classmethod
    def from_log_entry(cls, log_entry: str):
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


def get_coordinates(entries: list[str], log_date: date):
    """Parse log entries."""
    for line in entries:
        player_message = PlayerMessage.from_log_entry(line)
        if player_message:
            coord = CoordinateEntry.from_message(player_message.content)
            if coord:
                entry_dt = datetime.combine(log_date, player_message.time)
                coord.dt = entry_dt
                coord.username = player_message.username
                print(player_message)
                print(coord)


def read_from_logfile(log_file: Path):
    """Read from a SAVED log file, ending with .log.gz."""
    with gzip.open(log_file, "r") as f:
        # Boldly assume log file name is in the format: YYYY-MM-DD-n.log.gz
        log_date = date(*(int(i) for i in log_file.name.split("-")[:3]))
        get_coordinates(f.read().decode().splitlines(), log_date)


def read_from_latest(log_folder: Path, last_read: LastRead):
    """Read from the last line read in latest.log."""
    with open(Path(log_folder).joinpath("latest.log"), "r") as f:
        log_entries = f.read().splitlines()
        from_line = last_read.line_number + 1

        get_coordinates(log_entries[from_line:], date.today())
        last_read.update(line_number=len(log_entries))


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
    log_folder = Path(log_folder)
    log_files = sorted(f for f in os.listdir(log_folder) if f.endswith(".log.gz"))
    last_read = LastRead.load()

    # Nothing is read, this is the first run.
    if last_read is None:
        print("First run, scraping everything.")
        scrape_all(log_folder)
        return

    # Scrape log files that was just created.
    if last_read.log_file != log_files[-1]:
        print("New log file(s) rolled over.")
        new_index = log_files.index(last_read.log_file) + 1
        for log_file in log_files[new_index:]:
            read_from_logfile(log_folder / log_file)
        last_read.update(log_file=log_files[-1])

    # Scrape from latest.log.
    read_from_latest(log_folder, last_read)

    print(last_read)
    print(log_files)


if __name__ == "__main__":
    scrape_all("logs")
    # poll_logs("logs")
