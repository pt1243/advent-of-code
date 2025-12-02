from collections import defaultdict
from itertools import product

with open("./2015/resources/17.txt") as f:
    sizes = [int(size) for size in f.read().splitlines()]


def problem_1() -> None:
    total = 0
    for comb in product((True, False), repeat=len(sizes)):
        comb_total = 0
        for idx, include in enumerate(comb):  # faster than comprehension
            if include:
                comb_total += sizes[idx]
        if comb_total == 150:
            total += 1

    print(total)


def problem_2() -> None:
    num_ways: defaultdict[int, int] = defaultdict(int)
    for comb in product((True, False), repeat=len(sizes)):
        comb_total = 0
        for idx, include in enumerate(comb):  # faster than comprehension
            if include:
                comb_total += sizes[idx]
        if comb_total == 150:
            num_ways[sum(comb)] += 1

    print(num_ways[min(num_ways.keys())])
