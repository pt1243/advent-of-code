from itertools import batched, chain

import numpy as np
from more_itertools import mark_ends, split_after

with open("./2022/resources/22.txt") as f:
    text = f.read().rstrip()


def run_moves(layout: list[list[int | None]], connections: tuple[tuple[tuple[int, int, bool], ...], ...]) -> int:
    all_sides, move_sequence = text.split("\n\n")
    sides_lines = all_sides.splitlines()
    height, width = len(layout), len(layout[0])
    size = len(sides_lines) // height
    arr = np.zeros((6, size, size), bool)
    for row_list, lines_group in zip(layout, batched(sides_lines, size)):
        for col, side in enumerate(row_list):
            if side is not None:
                for row, line in enumerate(lines_group):
                    arr[side, row, :] = [char == "#" for char in line[size * col : size * (col + 1)]]
    side, row, col = map(int, np.unravel_index(np.argmin(arr), (6, size, size)))
    direction = 1
    directions = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
    for _, is_last, distance_and_direction in mark_ends(split_after(move_sequence, lambda c: c.isalpha())):
        if is_last:
            distance = int("".join(distance_and_direction))
        else:
            distance = int("".join(distance_and_direction[:-1]))
        for _ in range(distance):
            drow, dcol = directions[direction]
            next_row, next_col, next_direction, next_side = row + drow, col + dcol, direction, side
            if not (0 <= next_row < size and 0 <= next_col < size):  # new board
                next_side, next_direction, reverse = connections[side][direction]
                position_along_side = col if direction % 2 == 0 else row
                position_along_side = (size - 1 - position_along_side) if reverse else position_along_side
                next_col = position_along_side if next_direction % 2 == 0 else ((size - 1) * (next_direction == 3))
                next_row = position_along_side if next_direction % 2 != 0 else ((size - 1) * (next_direction == 0))
            if arr[next_side, next_row, next_col]:
                break
            row, col, direction, side = next_row, next_col, next_direction, next_side
        if not is_last:
            direction = (direction + (1 if distance_and_direction[-1] == "R" else -1)) % 4

    side_index = list(chain.from_iterable(layout)).index(side)
    side_row_index, side_col_index = map(int, np.unravel_index(side_index, (height, width)))
    final_row = side_row_index * size + row + 1
    final_col = side_col_index * size + col + 1
    final_facing = (direction - 1) % 4
    return 1000 * final_row + 4 * final_col + final_facing


def part_1() -> None:
    print(
        run_moves(
            [[None, 0, 1], [None, 2, None], [3, 4, None], [5, None, None]],
            (
                ((4, 0, False), (1, 1, False), (2, 2, False), (1, 3, False)),
                ((1, 0, False), (0, 1, False), (1, 2, False), (0, 3, False)),
                ((0, 0, False), (2, 1, False), (4, 2, False), (2, 3, False)),
                ((5, 0, False), (4, 1, False), (5, 2, False), (4, 3, False)),
                ((2, 0, False), (3, 1, False), (0, 2, False), (3, 3, False)),
                ((3, 0, False), (5, 1, False), (3, 2, False), (5, 3, False)),
            ),
        )
    )


def part_2() -> None:
    print(
        run_moves(
            [[None, 0, 1], [None, 2, None], [3, 4, None], [5, None, None]],
            (
                ((5, 1, False), (1, 1, False), (2, 2, False), (3, 1, True)),
                ((5, 0, False), (4, 3, True), (2, 3, False), (0, 3, False)),
                ((0, 0, False), (1, 0, False), (4, 2, False), (3, 2, False)),
                ((2, 1, False), (4, 1, False), (5, 2, False), (0, 1, True)),
                ((2, 0, False), (1, 3, True), (5, 3, False), (3, 3, False)),
                ((3, 0, False), (4, 0, False), (1, 2, False), (0, 2, False)),
            ),
        )
    )
