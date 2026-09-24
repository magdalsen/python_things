# Time Tracker Analytics – Reads time-tracking data from a CSV file and generates a report summarizing time spent across projects, clients, and other tags.


import csv
from typing import List, Dict

FILENAME_DATA = 'track.csv'

class Entry:
    def __init__(self, desc: str, time: int, tags: str) -> None:
        self.desc = desc
        self.time = time
        self.tags = tags

    def __repr__(self) -> str:
        return f"{self.desc} {self.time} {self.tags}"

def segregate_data(data: List[Entry]) -> Dict[str, int]:
    result = {}

    for row in data:
        tags = row.tags.split()  # ['klient-X', 'projekt-A', 'phone']

        for tag in tags:
            result[tag] = result.get(tag, 0) + row.time # słownik

    return result

def agregate_data(row: Dict[str, str]) -> Entry:
    return Entry(
        desc=row['desc'],
        time=int(row['time']),
        tags=row['tags'],
    )

def upload_data(filename: str) -> List[Entry]:
    with open(filename) as stream:
        reader = csv.DictReader(stream)
        all_data = [agregate_data(row) for row in reader]
    return all_data

def main() -> None:
    data = upload_data(FILENAME_DATA)
    summary = segregate_data(data)

    for tag, total in summary.items():
        print(tag, total)

if __name__ == "__main__":
    main()