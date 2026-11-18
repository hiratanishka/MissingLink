
import csv

from pathlib import Path


COLUMNS = [
    "Case ID",
    "Age",
    "Gender",
    "Missing Location",
    "Missing Since",
    "Description"
]


def save_records(records, filename="local_records.csv"):

    path = Path(filename)

    with path.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=COLUMNS,
            extrasaction="ignore"
        )

        writer.writeheader()

        for record in records:

            row = {}

            for column in COLUMNS:

                value = record.get(column)

                row[column] = (
                    "" if value is None else value
                )

            writer.writerow(row)

    return str(path)


def load_saved_records(filename="local_records.csv"):

    path = Path(filename)

    if not path.exists():
        return []

    with path.open(
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        return list(reader)
