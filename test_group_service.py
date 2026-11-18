
import unittest

from group_service import find_possible_groups


class TestGroupService(unittest.TestCase):

    def test_similar_records_grouped(self):

        records = [
            {
                "Case ID": "TEST001",
                "Age": 22,
                "Gender": "male",
                "Missing Location": "delhi",
                "Missing Since": None,
                "Description": "blue shirt black jeans"
            },
            {
                "Case ID": "TEST002",
                "Age": 22,
                "Gender": "male",
                "Missing Location": "delhi",
                "Missing Since": None,
                "Description": "blue shirt black jeans"
            }
        ]

        groups = find_possible_groups(records)

        self.assertEqual(len(groups), 1)
        self.assertEqual(len(groups[0]), 2)

    def test_different_locations(self):

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
                "Age": 22,
                "Gender": "male",
                "Missing Location": "mumbai",
                "Missing Since": None,
                "Description": "blue shirt"
            }
        ]

        groups = find_possible_groups(records)

        self.assertEqual(groups, [])

    def test_empty_records(self):

        self.assertEqual(
            find_possible_groups([]),
            []
        )


if __name__ == "__main__":
    unittest.main()
