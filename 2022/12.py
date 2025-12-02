import heapq
from collections import defaultdict

with open("./2022/resources/12.txt") as f:
    lines = f.read().splitlines()


def a_star(start_row: int, start_col: int, grid: list[list[int]]) -> int | None:
    width = len(lines[0])
    height = len(lines)
    end_row = next(i for i, line in enumerate(lines) if "E" in line)
    end_col = lines[end_row].index("E")

    start = (start_row, start_col)
    g_score: defaultdict[tuple[int, int], int] = defaultdict(lambda: 10**12)
    g_score[start] = 0
    f_score: defaultdict[tuple[int, int], int] = defaultdict(lambda: 10**12)
    f_score[start] = abs(end_row - start_row) + abs(end_col - start_col)

    open_set = [(0, start)]
    while open_set:
        _, current = heapq.heappop(open_set)
        if current == (end_row, end_col):
            return g_score[current]
        row, col = current
        current_value = grid[row][col]
        for drow, dcol in ((-1, 0), (0, 1), (1, 0), (0, -1)):
            new_row, new_col = row + drow, col + dcol
            if 0 <= new_row < height and 0 <= new_col < width and grid[new_row][new_col] - current_value <= 1:
                tentative_g_score = g_score[current] + 1
                neighbour = (new_row, new_col)
                if tentative_g_score < g_score[neighbour]:
                    g_score[neighbour] = tentative_g_score
                    f_score[neighbour] = tentative_g_score + abs(new_row - end_row) + abs(new_col - end_col)
                    heapq.heappush(open_set, (f_score[neighbour], neighbour))
    return None


def problem_1() -> None:
    start_row = next(i for i, line in enumerate(lines) if "S" in line)
    start_col = lines[start_row].index("S")
    grid = [[ord(c) - ord("a") if c not in "SE" else (0 if c == "S" else 26) for c in line] for line in lines]
    print(a_star(start_row, start_col, grid))


def problem_2() -> None:
    grid = [[ord(c) - ord("a") if c not in "SE" else (0 if c == "S" else 26) for c in line] for line in lines]
    print(
        min(
            dist
            for dist in (
                a_star(start_row, start_col, grid)
                for start_row, line in enumerate(lines)
                for start_col, char in enumerate(line)
                if char in "aS"
            )
            if dist is not None
        )
    )
