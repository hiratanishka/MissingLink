
import unittest

from search import (make_location_index, find_by_location,linear_search)
class TestSearch(unittest.TestCase):

    def test_location_index(self):

        records = [
            {
                "Case ID": "TEST001",
                "Missing Location": "delhi"
            },
            {
                "Case ID": "TEST002",
                "Missing Location": "noida"
            },
            {
                "Case ID": "TEST003",
                "Missing Location": "delhi"
            }
        ]

        index = make_location_index(records)

        self.assertEqual(len(index["delhi"]), 2)

    def test_find_location(self):

        records = [
            {
                "Case ID": "TEST001",
                "Missing Location": "delhi"
            }
        ]

        index = make_location_index(records)

        result = find_by_location(index, "DELHI")

        self.assertEqual(len(result), 1)

    def test_unknown_location(self):

        index = {}

        result = find_by_location(index, "mumbai")

        self.assertEqual(result, [])

    
    def linear_search(records, person, score_function, min_score=0):

        matches = []

        for record in records:

            score = score_function(person, record)

        if score >= min_score:
            matches.append({
                "record": record,
                "score": score
            })

        return matches



if __name__ == "__main__":
    unittest.main()
