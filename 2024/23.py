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
    print(sum(1 for g in groups_of_three if any(c.startswith("t") for c in g)))


def problem_2() -> None:
    connections: defaultdict[str, set[str]] = defaultdict(set)
    for line in lines:
        left, right = line.split("-")
        connections[left].add(right)
        connections[right].add(left)

    max_length = 0
    longest_group: set[str] = set()
    for start in connections:
        group = {start}
        while True:
            for other in connections:
                if all(other in connections[c] for c in group):
                    group.add(other)
                    break
            else:
                break
        length = len(group)
        if length > max_length:
            longest_group = group
            max_length = length
    print(",".join(sorted(longest_group)))
