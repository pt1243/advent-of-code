from itertools import pairwise, batched
import re


with open("./2022/resources/14.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    occupied: set[tuple[int, int]] = set()
    int_pattern = re.compile(r"-?\d+")
    for line in lines:
        ints = map(int, re.findall(int_pattern, line))
        for (col_1, row_1), (col_2, row_2) in pairwise(batched(ints, 2)):
            if col_1 == col_2:
                low, high = min(row_1, row_2), max(row_1, row_2)
                for row in range(low, high + 1):
                    occupied.add((row, col_1))
            else:
                low, high = min(col_1, col_2), max(col_1, col_2)
                for col in range(low, high + 1):
                    occupied.add((row_1, col))
    max_row = max(pos[0] for pos in occupied)

    sand = 0
    sand_falling = True
    while sand_falling:
        row, col = 0, 500
        while True:
            if row > max_row:
                sand_falling = False
                break
            if (row + 1, col) not in occupied:
                row += 1
            elif (row + 1, col - 1) not in occupied:
                row += 1
                col -= 1
            elif (row + 1, col + 1) not in occupied:
                row += 1
                col += 1
            else:
                occupied.add((row, col))
                sand += 1
                break
    print(sand)


def problem_2() -> None:
    occupied: set[tuple[int, int]] = set()
    int_pattern = re.compile(r"-?\d+")
    for line in lines:
        ints = map(int, re.findall(int_pattern, line))
        for (col_1, row_1), (col_2, row_2) in pairwise(batched(ints, 2)):
            if col_1 == col_2:
                low, high = min(row_1, row_2), max(row_1, row_2)
                for row in range(low, high + 1):
                    occupied.add((row, col_1))
            else:
                low, high = min(col_1, col_2), max(col_1, col_2)
                for col in range(low, high + 1):
                    occupied.add((row_1, col))
    floor = max(pos[0] for pos in occupied) + 2

    sand = 0
    sand_falling = True
    while sand_falling:
        row, col = 0, 500
        while True:
            if row + 1 == floor:
                occupied.add((row, col))
                sand += 1
                break
            if (row + 1, col) not in occupied:
                row += 1
            elif (row + 1, col - 1) not in occupied:
                row += 1
                col -= 1
            elif (row + 1, col + 1) not in occupied:
                row += 1
                col += 1
            else:
                occupied.add((row, col))
                sand += 1
                if (row, col) == (0, 500):
                    sand_falling = False
                break
    print(sand)
