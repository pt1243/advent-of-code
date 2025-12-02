from collections import defaultdict

with open("./2024/resources/23.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    connections: defaultdict[str, set[str]] = defaultdict(set)
    for line in lines:
        left, right = line.split("-")
        connections[left].add(right)
        connections[right].add(left)

    groups_of_three: set[frozenset[str]] = set()
    for first, first_connections in connections.items():
        for second in first_connections:
            for third in connections[second]:
                if first in connections[third]:
                    groups_of_three.add(frozenset({first, second, third}))
    print(sum(any(computer.startswith("t") for computer in g) for g in groups_of_three))


def problem_2() -> None:
    connections: defaultdict[str, set[str]] = defaultdict(set)
    for line in lines:
        left, right = line.split("-")
        connections[left].add(right)
        connections[right].add(left)

    largest_clique: set[str] = set()
    largest_clique_size = 0

    def bron_kerbosch(R: set[str], P: set[str], X: set[str]) -> None:
        nonlocal largest_clique_size, largest_clique
        if not P and not X:
            if len(R) > largest_clique_size:
                largest_clique_size = len(R)
                largest_clique = R
            return
        u = next(iter(P | X))  # pivot
        for v in P - connections[u]:
            bron_kerbosch(R | {v}, P & connections[v], X & connections[v])
            P -= {v}
            X |= {v}

    bron_kerbosch(set(), set(connections), set())
    print(",".join(sorted(largest_clique)))
