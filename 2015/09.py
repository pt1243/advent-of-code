from itertools import pairwise, permutations
from collections import defaultdict


with open("./2015/resources/9.txt") as f:
    all_distances = f.read().splitlines()


def problem_1() -> None:
    distances: defaultdict[str, defaultdict[str, int]] = defaultdict(lambda: defaultdict(int))
    for entry in all_distances:
        start, _, end, _, dist = entry.split()
        distances[start][end] = int(dist)
        distances[end][start] = int(dist)

    print(min(sum(distances[start][end] for (start, end) in pairwise(route)) for route in permutations(distances)))


def problem_2() -> None:
    distances: defaultdict[str, defaultdict[str, int]] = defaultdict(lambda: defaultdict(int))
    for entry in all_distances:
        start, _, end, _, dist = entry.split()
        distances[start][end] = int(dist)
        distances[end][start] = int(dist)

    print(max(sum(distances[start][end] for (start, end) in pairwise(route)) for route in permutations(distances)))
