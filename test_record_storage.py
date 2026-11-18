
import unittest

from pathlib import Path
from tempfile import TemporaryDirectory

from record_storage import (
    save_records,
    load_saved_records
)


class TestRecordStorage(unittest.TestCase):

    def test_save_and_load(self):

        records = [
            {
                "Case ID": "TEST001",
                "Age": 22,
                "Gender": "male",
                "Missing Location": "delhi",
                "Missing Since": "2026-11-10",
                "Description": "blue shirt"
            }
        ]

        with TemporaryDirectory() as folder:

            path = Path(folder) / "test_records.csv"

            save_records(records, path)

            loaded = load_saved_records(path)

            self.assertEqual(len(loaded), 1)

            self.assertEqual(
                loaded[0]["Case ID"],
                "TEST001"
            )

            self.assertEqual(
                loaded[0]["Missing Location"],
                "delhi"
            )

    def test_missing_file(self):

        with TemporaryDirectory() as folder:

            path = Path(folder) / "missing.csv"

            result = load_saved_records(path)

            self.assertEqual(result, [])

    def test_empty_records(self):

        with TemporaryDirectory() as folder:

            path = Path(folder) / "empty.csv"

            save_records([], path)

            loaded = load_saved_records(path)

            self.assertEqual(loaded, [])


if __name__ == "__main__":
    unittest.main()
