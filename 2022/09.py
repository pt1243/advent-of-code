from itertools import pairwise
from typing import cast


with open("./2022/resources/9.txt") as f:
    lines = f.read().splitlines()


def get_move(head_row: int, head_col: int, tail_row: int, tail_col: int) -> tuple[int, int]:
    row_diff = head_row - tail_row
    col_diff = head_col - tail_col

    if row_diff == 2:
        if col_diff == 0:
            return 1, 0
        return 1, (1 if col_diff > 0 else -1)
    if row_diff == 1:
        if col_diff == 2:
            return 1, 1
        elif col_diff == -2:
            return 1, -1
        else:
            return 0, 0
    if row_diff == -2:
        if col_diff == 0:
            return -1, 0
        return -1, (1 if col_diff > 0 else -1)
    if row_diff == -1:
        if col_diff == 2:
            return -1, 1
        elif col_diff == -2:
            return -1, -1
        return 0, 0
    if col_diff > 1:
        return 0, 1
    if col_diff < -1:
        return 0, -1
    return 0, 0


def problem_1() -> None:
    head_row, head_col = 0, 0
    tail_row, tail_col = 0, 0
    directions = {"U": (-1, 0), "R": (0, 1), "D": (1, 0), "L": (0, -1)}
    seen = {(tail_row, tail_col)}
    for line in lines:
        direction, dist = line.split()
        drow, dcol = directions[direction]
        for _ in range(int(dist)):
            head_row += drow
            head_col += dcol
            tail_drow, tail_dcol = get_move(head_row, head_col, tail_row, tail_col)
            tail_row += tail_drow
            tail_col += tail_dcol
            seen.add((tail_row, tail_col))
    print(len(seen))


def problem_2() -> None:
    positions = [[0, 0] for _ in range(10)]
    directions = {"U": (-1, 0), "R": (0, 1), "D": (1, 0), "L": (0, -1)}
    seen = {(0, 0)}
    for line in lines:
        direction, dist = line.split()
        drow, dcol = directions[direction]
        for _ in range(int(dist)):
            head = positions[0]
            head[0] += drow
            head[1] += dcol
            for head, tail in pairwise(positions):
                drow_tail, dcol_tail = get_move(head[0], head[1], tail[0], tail[1])
                tail[0] += drow_tail
                tail[1] += dcol_tail
            seen.add(cast(tuple[int, int], tuple(positions[-1])))
    print(len(seen))
