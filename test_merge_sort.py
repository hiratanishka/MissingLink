
import unittest

from merge_sort import merge_sort


class TestMergeSort(unittest.TestCase):

    def test_descending_order(self):

        records = [
            {"score": 60},
            {"score": 90},
            {"score": 40},
            {"score": 80}
        ]

        result = merge_sort(records)

        self.assertEqual(
            [item["score"] for item in result],
            [90, 80, 60, 40]
        )

    def test_empty(self):

        self.assertEqual(merge_sort([]), [])

    def test_same_scores(self):

        records = [
            {"score": 80, "id": "A"},
            {"score": 80, "id": "B"}
        ]

        result = merge_sort(records)

        self.assertEqual(
            [item["id"] for item in result],
            ["A", "B"]
        )

    def test_original_list_unchanged(self):

        records = [
            {"score": 10},
            {"score": 90}
        ]

        merge_sort(records)

        self.assertEqual(
            [item["score"] for item in records],
            [10, 90]
        )


if __name__ == "__main__":
    unittest.main()
