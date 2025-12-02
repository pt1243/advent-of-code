import bisect
import heapq
from collections import defaultdict

with open("./2024/resources/18.txt") as f:
    lines = f.read().splitlines()


def a_star(corrupted: set[tuple[int, int]]) -> int | None:
    start = (0, 0)
    end_row, end_col = 70, 70
    g_score: defaultdict[tuple[int, int], int] = defaultdict(lambda: 10**12)
    g_score[start] = 0
    f_score: defaultdict[tuple[int, int], int] = defaultdict(lambda: 10**12)
    f_score[start] = end_row + end_col
    open_set = [(0, start)]
    directions = ((-1, 0), (0, 1), (1, 0), (0, -1))

    while open_set:
        _, current = heapq.heappop(open_set)
        row, col = current
        if row == end_row and col == end_col:
            return g_score[current]
        for drow, dcol in directions:
            new_row = row + drow
            new_col = col + dcol
            if 0 <= new_row <= end_row and 0 <= new_col <= end_col and (new_row, new_col) not in corrupted:
                tentative_g_score = g_score[current] + 1
                new = (new_row, new_col)
                if tentative_g_score < g_score[new]:
                    g_score[new] = tentative_g_score
                    f_score[new] = tentative_g_score + end_row - new_row + end_col - new_col
                    heapq.heappush(open_set, (f_score[new], new))
    return None


def problem_1() -> None:
    corrupted: set[tuple[int, int]] = set()
    for line in lines[:1024]:
        row_str, col_str = line.split(",")
        corrupted.add((int(row_str), int(col_str)))
    print(a_star(corrupted))


def problem_2() -> None:
    corrupted: list[tuple[int, int]] = []
    for line in lines:
        row_str, col_str = line.split(",")
        corrupted.append((int(row_str), int(col_str)))

    print(
        lines[
            bisect.bisect_left(list(range(len(corrupted))), True, key=lambda i: a_star(set(corrupted[: i + 1])) is None)
        ]
    )
