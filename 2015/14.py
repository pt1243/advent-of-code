from collections.abc import Iterator
from itertools import cycle

with open("./2015/resources/14.txt") as f:
    lines = f.read().splitlines()


def part_1() -> None:
    all_reindeer: dict[str, Iterator[int]] = {}
    for line in lines:
        split = line.split()
        reindeer = split[0]
        speed = int(split[3])
        flying_time = int(split[6])
        rest_time = int(split[13])
        all_reindeer[reindeer] = cycle([speed for _ in range(flying_time)] + [0 for _ in range(rest_time)])

    distances = {r: 0 for r in all_reindeer}
    for _ in range(2503):
        for reindeer, iterator in all_reindeer.items():
            distances[reindeer] += next(iterator)

    print(max(distances.values()))


def part_2() -> None:
    all_reindeer: dict[str, Iterator[int]] = {}
    for line in lines:
        split = line.split()
        reindeer = split[0]
        speed = int(split[3])
        flying_time = int(split[6])
        rest_time = int(split[13])
        all_reindeer[reindeer] = cycle([speed for _ in range(flying_time)] + [0 for _ in range(rest_time)])

    distances = {r: 0 for r in all_reindeer}
    points = {r: 0 for r in all_reindeer}
    for _ in range(2503):
        for reindeer, iterator in all_reindeer.items():
            distances[reindeer] += next(iterator)
        for reindeer in points:
            if distances[reindeer] == max(distances.values()):
                points[reindeer] += 1

    print(max(points.values()))
