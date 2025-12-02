from itertools import pairwise

from more_itertools import split_when

with open("./2020/resources/10.txt") as f:
    all_adapters = {int(x) for x in f.read().splitlines()}


def part_1() -> None:
    all_adapters.add(0)
    all_adapters.add(max(all_adapters) + 3)
    one_jolt_differences = 0
    three_jolt_differences = 0
    for a1, a2 in pairwise(sorted(all_adapters)):
        if a2 - a1 == 1:
            one_jolt_differences += 1
        elif a2 - a1 == 3:
            three_jolt_differences += 1
    print(one_jolt_differences * three_jolt_differences)


def part_2() -> None:
    all_adapters.add(0)
    all_adapters.add(max(all_adapters) + 3)
    total = 1
    for group in split_when(sorted(all_adapters), lambda a1, a2: a2 - a1 == 3):
        if len(group) == 3:
            total *= 2
        elif len(group) == 4:
            total *= 4
        elif len(group) == 5:
            total *= 7
    print(total)
