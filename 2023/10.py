import sys
from enum import Enum

import numpy as np

sys.setrecursionlimit(10**6)


with open("./2023/resources/10.txt") as f:
    lines = f.read().splitlines()


class Direction(Enum):
    N = (-1, 0)
    E = (0, 1)
    S = (1, 0)
    W = (0, -1)


next_direction = {
    "|": {Direction.S: Direction.S, Direction.N: Direction.N},
    "-": {Direction.E: Direction.E, Direction.W: Direction.W},
    "L": {Direction.S: Direction.E, Direction.W: Direction.N},
    "J": {Direction.S: Direction.W, Direction.E: Direction.N},
    "7": {Direction.N: Direction.W, Direction.E: Direction.S},
    "F": {Direction.N: Direction.E, Direction.W: Direction.S},
}


def problem_1() -> None:
    for row, line in enumerate(lines):
        if "S" in line:
            start_row = row
            start_col = line.index("S")

    valid_north = ("|", "7", "F")
    valid_west = ("-", "L", "F")

    if lines[start_row - 1][start_col] in valid_north:
        direction = Direction.N
    elif lines[start_row][start_col - 1] in valid_west:
        direction = Direction.W
    else:
        direction = Direction.E
    distance = 0

    row, col = start_row, start_col
    while True:
        row_step, col_step = direction.value
        row += row_step
        col += col_step
        if (row, col) == (start_row, start_col):
            break
        distance += 1
        direction = next_direction[lines[row][col]][direction]
    print(distance // 2 + (1 if distance % 2 == 1 else 0))


def problem_2() -> None:
    for row, line in enumerate(lines):
        if "S" in line:
            start_row = row
            start_col = line.index("S")

    valid_north = ("|", "7", "F")
    valid_east = ("-", "J", "7")
    valid_west = ("-", "L", "F")

    initial_line = lines[start_row]
    start_char = initial_line[start_col]

    if lines[start_row - 1][start_col] in valid_north:
        direction = Direction.N
        if start_char in valid_east:
            replacement_char = "L"
        elif start_char in valid_west:
            replacement_char = "J"
        else:
            replacement_char = "|"
    elif lines[start_row][start_col - 1] in valid_west:
        direction = Direction.W
        if start_char in valid_east:
            replacement_char = "-"
        else:
            replacement_char = "7"
    else:
        direction = Direction.E
        replacement_char = "F"

    lines[start_row] = initial_line[:start_col] + replacement_char + initial_line[start_col + 1 :]

    loop_members = {(start_row, start_col)}
    row, col = start_row, start_col
    while True:
        row_step, col_step = direction.value
        row += row_step
        col += col_step
        if (row, col) == (start_row, start_col):
            break
        loop_members.add((row, col))
        direction = next_direction[lines[row][col]][direction]

    expanded_replacements = {
        "|": np.array([[0, 1, 0], [0, 1, 0], [0, 1, 0]]),
        "-": np.array([[0, 0, 0], [1, 1, 1], [0, 0, 0]]),
        "L": np.array([[0, 1, 0], [0, 1, 1], [0, 0, 0]]),
        "J": np.array([[0, 1, 0], [1, 1, 0], [0, 0, 0]]),
        "7": np.array([[0, 0, 0], [1, 1, 0], [0, 1, 0]]),
        "F": np.array([[0, 0, 0], [0, 1, 1], [0, 1, 0]]),
        "empty": np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]),
    }

    grid = np.zeros((len(lines) * 3, len(lines[0]) * 3), dtype=int)

    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if (row, col) not in loop_members:
                grid[row * 3 : row * 3 + 3, col * 3 : col * 3 + 3] = expanded_replacements["empty"]
            else:
                grid[row * 3 : row * 3 + 3, col * 3 : col * 3 + 3] = expanded_replacements[char]

    max_row, max_col = grid.shape

    def floodfill(row: int, col: int) -> None:
        grid[row, col] = 1
        if row > 0 and not grid[row - 1, col]:
            floodfill(row - 1, col)
        if row < max_row - 1 and not grid[row + 1, col]:
            floodfill(row + 1, col)
        if col > 0 and not grid[row, col - 1]:
            floodfill(row, col - 1)
        if col < max_col - 1 and not grid[row, col + 1]:
            floodfill(row, col + 1)

    floodfill(0, 0)

    print(len(lines) * len(lines[0]) - np.count_nonzero(grid[1::3, 1::3]))
