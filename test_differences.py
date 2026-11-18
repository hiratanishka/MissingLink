
import unittest

from check_differences import check_differences


class TestDifferences(unittest.TestCase):

    def test_same_details(self):

        person1 = {"Age": 22, "Gender": "male"}
        person2 = {"Age": 23, "Gender": "male"}

        result = check_differences(person1, person2)

        self.assertEqual(result, [])

    def test_large_age_difference(self):

        person1 = {"Age": 22, "Gender": "male"}
        person2 = {"Age": 55, "Gender": "male"}

        result = check_differences(person1, person2)

        self.assertIn("Large age difference", result)

    def test_different_gender(self):

        person1 = {"Age": 22, "Gender": "male"}
        person2 = {"Age": 22, "Gender": "female"}

        result = check_differences(person1, person2)

        self.assertIn("Different gender", result)

    def test_unknown_details(self):

        person1 = {"Age": None, "Gender": ""}
        person2 = {"Age": 25, "Gender": "male"}

        result = check_differences(person1, person2)

        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
