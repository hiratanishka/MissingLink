
import unittest

from search import (
    make_location_index,
    find_by_location,
    linear_search
)

from match_score import calculate_score


class TestFullSearch(unittest.TestCase):

    def test_matching_records(self):

        records = [
            {
                "Case ID": "TEST001",
                "Age": 22,
                "Gender": "male",
                "Missing Location": "delhi",
                "Missing Since": None,
                "Description": "blue shirt"
            },
            {
                "Case ID": "TEST002",
                "Age": 45,
                "Gender": "female",
                "Missing Location": "mumbai",
                "Missing Since": None,
                "Description": "red jacket"
            }
        ]

        person = records[0].copy()

        index = make_location_index(records)

        candidates = find_by_location(
            index,
            "delhi"
        )

        results = linear_search(
            candidates,
            person,
            calculate_score,
            min_score=50
        )

        self.assertEqual(len(results), 1)

        self.assertEqual(
            results[0]["record"]["Case ID"],
            "TEST001"
        )

        self.assertEqual(results[0]["score"], 85)

    def test_no_matches(self):

        results = linear_search(
            [],
            {"Age": 22},
            calculate_score,
            min_score=50
        )

        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()
