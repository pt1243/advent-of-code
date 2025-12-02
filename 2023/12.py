from functools import cache
from itertools import repeat

with open("./2023/resources/12.txt") as f:
    lines = f.read().splitlines()


@cache
def num_possibilities(record: str, groups: tuple[int, ...]) -> int:
    if not groups:
        return int("#" not in record)
    if not record:
        return 0

    char = record[0]
    total = 0
    if char in ".?":  # continue from the next character
        total += num_possibilities(record[1:], groups)
    if char in "#?":
        first_group = record[: groups[0]].replace("?", "#")  # treat the first group as all #
        if first_group != groups[0] * "#":  # if the first group is not the correct length
            return total
        if len(record) == groups[0]:  # if the first group is the size of the record, and it is the only group
            total += int(len(groups) == 1)
        elif record[groups[0]] in ".?":  # if the next character after the group could split the groups
            total += num_possibilities(record[groups[0] + 1 :], groups[1:])
    return total


def problem_1() -> None:
    total_arrangements = 0
    for line in lines:
        springs, groups_str = line.split()
        groups = tuple(int(x) for x in groups_str.split(","))
        total_arrangements += num_possibilities(springs, groups)
    print(total_arrangements)


def problem_2() -> None:
    total_arrangements = 0
    for line in lines:
        springs, groups_str = line.split()
        springs = "?".join(repeat(springs, 5))
        groups = tuple(int(x) for x in groups_str.split(",")) * 5
        total_arrangements += num_possibilities(springs, groups)
    print(total_arrangements)
