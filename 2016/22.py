from typing import NamedTuple


with open('./2016/resources/22.txt') as f:
    lines = [line.strip() for line in f][2:]


class Node(NamedTuple):
    x: int
    y: int
    size: int
    used: int
    avail: int


def problem_1() -> None:
    all_nodes: list[Node] = []
    for line in lines:
        split = line.split()
        all_nodes.append(Node(
            int(split[0][split[0].index("-")+2:split[0].rindex("-")]),
            int(split[0][split[0].rindex("-")+2:]),
            int(split[1][:-1]),
            int(split[2][:-1]),
            int(split[3][:-1]),
        ))
    found_viable_pairs = 0
    for a in all_nodes:
        for b in all_nodes:
            if a.used == 0:
                continue
            if a == b:
                continue
            if a.used <= b.avail:
                found_viable_pairs += 1
    print(found_viable_pairs)
