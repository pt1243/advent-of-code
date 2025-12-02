from itertools import batched

with open("./2022/resources/3.txt") as f:
    lines = f.read().splitlines()


def part_1() -> None:
    total = 0
    for line in lines:
        left, right = set(line[: len(line) // 2]), set(line[len(line) // 2 :])
        common = (left & right).pop()
        total += ord(common.lower()) - ord("a") + 1
        if common.isupper():
            total += 26
    print(total)


def part_2() -> None:
    total = 0
    for line_1, line_2, line_3 in batched(lines, 3):
        common = (set(line_1) & set(line_2) & set(line_3)).pop()
        total += ord(common.lower()) - ord("a") + 1
        if common.isupper():
            total += 26
    print(total)
