
import unittest

from match_score import calculate_score, get_word_score


class TestMatchScore(unittest.TestCase):

    def test_common_words(self):

        score = get_word_score(
            "blue shirt black jeans",
            "blue shirt white jeans"
        )

        self.assertEqual(score, 0.6)

    def test_perfect_match(self):

        person = {
            "Age": 22,
            "Gender": "male",
            "Missing Location": "delhi",
            "Missing Since": "2026-11-10",
            "Description": "blue shirt"
        }

        self.assertEqual(
            calculate_score(person, person),
            100
        )

    def test_different_age(self):

        person1 = {
            "Age": 22,
            "Gender": "male",
            "Missing Location": "delhi",
            "Missing Since": "2026-11-10",
            "Description": "blue shirt"
        }

        person2 = person1.copy()
        person2["Age"] = 23

        self.assertEqual(
            calculate_score(person1, person2),
            90
        )


if __name__ == "__main__":
    unittest.main()
