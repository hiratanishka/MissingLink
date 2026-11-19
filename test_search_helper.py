
import unittest

from search_helper import suggest_next_detail


class TestSearchHelper(unittest.TestCase):

    def test_missing_description(self):

        person = {
            "Age": 22,
            "Gender": "male",
            "Missing Location": "delhi",
            "Missing Since": "2026-11-10",
            "Description": ""
        }

        result = suggest_next_detail(person, [{}])

        self.assertIn("description", result.lower())

    def test_missing_location(self):

        person = {
            "Age": 22,
            "Gender": "male",
            "Missing Location": "",
            "Missing Since": "2026-11-10",
            "Description": "blue shirt"
        }

        result = suggest_next_detail(person, [{}])

        self.assertIn("location", result.lower())

    def test_all_details(self):

        person = {
            "Age": 22,
            "Gender": "male",
            "Missing Location": "delhi",
            "Missing Since": "2026-11-10",
            "Description": "blue shirt"
        }

        result = suggest_next_detail(person, [{}])

        self.assertEqual(
            result,
            "All main details are provided."
        )

    def test_empty_dataset(self):

        result = suggest_next_detail({}, [])

        self.assertIn("Load records", result)


if __name__ == "__main__":
    unittest.main()
