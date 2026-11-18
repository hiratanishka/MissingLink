
import unittest

from groups import UnionFind, make_groups


class TestGroups(unittest.TestCase):

    def test_union(self):

        uf = UnionFind(4)

        uf.union(0, 1)
        uf.union(2, 3)

        self.assertEqual(
            uf.find(0),
            uf.find(1)
        )

        self.assertNotEqual(
            uf.find(0),
            uf.find(2)
        )

    def test_make_groups(self):

        groups = make_groups(
            4,
            [(0, 1), (2, 3)]
        )

        normalized = sorted(
            sorted(group) for group in groups
        )

        self.assertEqual(
            normalized,
            [[0, 1], [2, 3]]
        )

    def test_no_pairs(self):

        groups = make_groups(3, [])

        self.assertEqual(len(groups), 3)


if __name__ == "__main__":
    unittest.main()
