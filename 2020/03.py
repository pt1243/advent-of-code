from itertools import batched

with open("./2020/resources/3.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    width = len(lines[0])
    trees_hit = 0
    for i, row in enumerate(lines):
        if row[(i * 3) % width] == "#":
            trees_hit += 1
    print(trees_hit)


def problem_2() -> None:
    width = len(lines[0])
    prod = 1
    for slope in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2)):
        trees_hit = 0
        for i, row_group in enumerate(batched(lines, slope[1])):
            row = row_group[0]
            if row[(i * slope[0]) % width] == "#":
                trees_hit += 1
        prod *= trees_hit
    print(prod)
