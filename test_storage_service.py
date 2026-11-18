
import unittest

from pathlib import Path
from tempfile import TemporaryDirectory
from datetime import date

from storage_service import (
    save_local_dataset,
    open_local_dataset
)


class TestStorageService(unittest.TestCase):

    def test_save_and_clean_load(self):

        records = [
            {
                "Case ID": "TEST001",
                "Age": 22,
                "Gender": "male",
                "Missing Location": "delhi",
                "Missing Since": date(2026, 11, 10),
                "Description": "blue shirt"
            }
        ]

        with TemporaryDirectory() as folder:

            path = Path(folder) / "records.csv"

            save_local_dataset(records, path)

            loaded = open_local_dataset(path)

            self.assertEqual(len(loaded), 1)
            self.assertEqual(loaded[0]["Age"], 22)

            self.assertEqual(
                loaded[0]["Missing Since"],
                date(2026, 11, 10)
            )

    def test_missing_file(self):

        with TemporaryDirectory() as folder:

            path = Path(folder) / "missing.csv"

            self.assertEqual(open_local_dataset(path), [])


if __name__ == "__main__":
    unittest.main()
