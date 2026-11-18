
from record_storage import (
    save_records,
    load_saved_records
)

from data_cleaning import clean_records


def save_local_dataset(records, filename="local_records.csv"):

    return save_records(records, filename)


def open_local_dataset(filename="local_records.csv"):

    records = load_saved_records(filename)

    if not records:
        return []

    return clean_records(records)
