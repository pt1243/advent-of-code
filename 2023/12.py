from more_itertools import split_when
from itertools import product


with open('./2023/resources/12.txt') as f:
    lines = [line.strip() for line in f]


# lines = [
#     "???.### 1,1,3",
#     ".??..??...?##. 1,1,3",
#     "?#?#?#?#?#?#?#? 1,3,1,6",
#     "????.#...#... 4,1,1",
#     "????.######..#####. 1,6,5",
#     "?###???????? 3,2,1",
# ]


def problem_1() -> None:
    total_arrangements = 0
    for line in lines:
        springs, groups = line.split()
        groups = [int(x) for x in groups.split(",")]
        options = [(c,) if c != "?" else ("#", ".") for c in springs ]
        for possibility in product(*options):
            all_groups = split_when(possibility, lambda x, y: x != y)
            relevant = [len(g) for g in all_groups if g[0] == "#"]
            if relevant == groups:
                total_arrangements += 1
    print(total_arrangements)


def problem_2() -> None:
    pass
