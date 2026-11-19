
import unittest

from smart_case_link import find_case_links


class TestSmartCaseLink(unittest.TestCase):

    def test_cross_location_link(self):

        person = {
            "Case ID": "TEST001",
            "Age": 22,
            "Gender": "male",
            "Missing Location": "delhi",
            "Missing Since": None,
            "Description": "blue shirt black jeans"
        }

        records = [
            {
                "Case ID": "TEST002",
                "Age": 22,
                "Gender": "male",
                "Missing Location": "noida",
                "Missing Since": None,
                "Description": "blue shirt black jeans"
            }
        ]

        links = find_case_links(person, records)

        self.assertEqual(len(links), 1)
        self.assertEqual(links[0]["score"], 60)

    def test_same_location_skipped(self):

        person = {
            "Age": 22,
            "Gender": "male",
            "Missing Location": "delhi",
            "Missing Since": None,
            "Description": "blue shirt"
        }

        records = [person.copy()]

        self.assertEqual(
            find_case_links(person, records),
            []
        )

    def test_empty_records(self):

        person = {"Missing Location": "delhi"}

        self.assertEqual(
            find_case_links(person, []),
            []
        )


if __name__ == "__main__":
    unittest.main()
