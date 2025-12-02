import heapq
from collections import defaultdict

import numpy as np
import numpy.typing as npt

with open("./2021/resources/15.txt") as f:
    risk_levels = np.array([[int(char) for char in line] for line in f.read().splitlines()])


def a_star(risk_levels: npt.NDArray[np.int_]) -> int:
    width = len(risk_levels[0])
    height = len(risk_levels)
    open_set = [(0, 0, 0)]
    g_score: defaultdict[tuple[int, int], int] = defaultdict(lambda: 10**6)
    g_score[(0, 0)] = 0
    f_score: defaultdict[tuple[int, int], int] = defaultdict(lambda: 10**6)
    f_score[(0, 0)] = 0
    while open_set:
        _, row, col = heapq.heappop(open_set)
        if row == height - 1 and col == width - 1:
            return g_score[row, col]
        for drow, dcol in ((-1, 0), (0, -1), (0, 1), (1, 0)):
            new_row = row + drow
            new_col = col + dcol
            if new_row < 0 or new_row >= height or new_col < 0 or new_col >= width:
                continue
            tentative_g_score = g_score[row, col] + risk_levels[new_row][new_col]
            if tentative_g_score < g_score[new_row, new_col]:
                g_score[new_row, new_col] = tentative_g_score
                f_score[new_row, new_col] = tentative_g_score + (width - 1 - new_col) + (height - 1 - new_row)
                heapq.heappush(open_set, (f_score[new_row, new_col], new_row, new_col))
    raise ValueError("did not reach bottom right corner")


def problem_1() -> None:
    print(a_star(risk_levels))


def problem_2() -> None:
    height, width = risk_levels.shape
    expanded_risk_levels = np.empty((height * 5, width * 5), int)
    for offset in range(9):
        adjusted_risk_levels = risk_levels + offset
        adjusted_risk_levels[adjusted_risk_levels > 9] -= 9
        for row in range(5):
            for col in range(5):
                if row + col == offset:
                    expanded_risk_levels[row * height : (row + 1) * height, col * width : (col + 1) * width] = (
                        adjusted_risk_levels
                    )
    print(a_star(expanded_risk_levels))
