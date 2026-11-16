import unittest

from data_cleaning import (
    clean_text,
    clean_age,
    clean_date,
    clean_records
)


class TestCleaning(unittest.TestCase):

    def test_text(self):

        self.assertEqual(
            clean_text(" DELHI "),
            "delhi"
        )

    def test_age(self):

        self.assertEqual(clean_age("22"), 22)

        self.assertIsNone(clean_age("unknown"))

        self.assertIsNone(clean_age("200"))

    def test_date(self):

        self.assertEqual(
            str(clean_date("10112026")),
            "2026-11-10"
        )

    def test_record(self):

        records = [
            {
                "Case ID": "TEST001",
                "Age": "22",
                "Gender": "MALE",
                "Missing Location": " DELHI ",
                "Missing Since": "10112026",
                "Description": "Blue Shirt"
            }
        ]

        result = clean_records(records)

        self.assertEqual(
            result[0]["Missing Location"],
            "delhi"
        )

    def test_missing_columns(self):

        with self.assertRaises(ValueError):

            clean_records([
                {"Age": 22}
            ])


if __name__ == "__main__":
    unittest.main()