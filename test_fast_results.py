
import unittest

from fast_results import top_matches

class TestFastResults(unittest.TestCase):

    def test_top_three(self):

        scores = [60, 85, 72, 95, 40, 90]

        results = [
            {
                "score": score,
                "record": {"Case ID": str(index)}
            }
            for index, score in enumerate(scores)
        ]

        best = top_matches(results, limit=3)

        self.assertEqual(
            [item["score"] for item in best],
            [95, 90, 85]
        )

    def test_empty(self):

        self.assertEqual(top_matches([], limit=10), [])

    def test_fewer_results(self):

        results = [
            {"score": 70, "record": {"Case ID": "A"}},
            {"score": 90, "record": {"Case ID": "B"}}
        ]

        best = top_matches(results, limit=10)

        self.assertEqual(len(best), 2)


if __name__ == "__main__":
    unittest.main()
