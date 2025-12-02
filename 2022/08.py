from more_itertools import split_after

with open("./2022/resources/8.txt") as f:
    trees = [[int(x) for x in line] for line in f.read().splitlines()]


def part_1() -> None:
    width, height = len(trees[0]), len(trees)
    visible = 0
    for row, line in enumerate(trees):
        for col, tree in enumerate(line):
            if (
                all(trees[row][c] < tree for c in range(col))
                or all(trees[row][c] < tree for c in range(col + 1, width))
                or all(trees[r][col] < tree for r in range(row))
                or all(trees[r][col] < tree for r in range(row + 1, height))
            ):
                visible += 1
    print(visible)


def part_2() -> None:
    width, height = len(trees[0]), len(trees)
    max_scenic_score = 0
    for row, line in enumerate(trees):
        for col, tree in enumerate(line):
            up = len(next(split_after((trees[r][col] for r in range(row - 1, -1, -1)), lambda x: x >= tree), ()))
            down = len(next(split_after((trees[r][col] for r in range(row + 1, height)), lambda x: x >= tree), ()))
            left = len(next(split_after((trees[row][c] for c in range(col - 1, -1, -1)), lambda x: x >= tree), ()))
            right = len(next(split_after((trees[row][c] for c in range(col + 1, width)), lambda x: x >= tree), ()))
            max_scenic_score = max(max_scenic_score, up * down * left * right)
    print(max_scenic_score)
