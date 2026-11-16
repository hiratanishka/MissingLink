
import unittest

from io import StringIO

from data_loader import load_data
from data_cleaning import clean_records


class TestIntegration(unittest.TestCase):

    def test_load_and_clean(self):

        sample = StringIO(
            "Case ID,Age,Gender,"
            "Missing Location,Missing Since,"
            "Description\n"
            "TEST001,22,MALE, DELHI ,"
            "10112026,Blue Shirt"
        )

        raw = load_data(sample, "sample.csv")

        records = clean_records(raw)

        self.assertEqual(len(records), 1)

        self.assertEqual(records[0]["Age"], 22)

        self.assertEqual(
            records[0]["Missing Location"],
            "delhi"
        )

        self.assertEqual(
            records[0]["Gender"],
            "male"
        )


if __name__ == "__main__":
    unittest.main()
