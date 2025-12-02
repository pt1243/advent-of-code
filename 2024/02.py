from itertools import pairwise

with open("./2024/resources/2.txt") as f:
    lines = [[int(x) for x in line.split()] for line in f.read().splitlines()]


def is_safe(line: list[int]) -> bool:
    if not (sorted(line) == line or sorted(line) == line[::-1]):
        return False
    if not all(1 <= abs(a - b) <= 3 for a, b in pairwise(line)):
        return False
    return True


def problem_1() -> None:
    print(sum(is_safe(line) for line in lines))


def problem_2() -> None:
    print(sum(any(is_safe(line[:i] + line[i + 1 :]) for i in range(len(line))) for line in lines))
