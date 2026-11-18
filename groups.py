
class UnionFind:

    def __init__(self, size):

        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, x):

        if self.parent[x] != x:
            self.parent[x] = self.find(
                self.parent[x]
            )

        return self.parent[x]

    def union(self, a, b):

        root_a = self.find(a)
        root_b = self.find(b)

        if root_a == root_b:
            return False

        if self.rank[root_a] < self.rank[root_b]:
            root_a, root_b = root_b, root_a

        self.parent[root_b] = root_a

        if self.rank[root_a] == self.rank[root_b]:
            self.rank[root_a] += 1

        return True


def make_groups(size, pairs):

    uf = UnionFind(size)

    for a, b in pairs:
        uf.union(a, b)

    groups = {}

    for index in range(size):

        root = uf.find(index)

        if root not in groups:
            groups[root] = []

        groups[root].append(index)

    return list(groups.values())
