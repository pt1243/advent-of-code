import heapq
from collections import defaultdict
from functools import cache

with open("./2022/resources/24.txt") as f:
    lines = f.read().splitlines()


def a_star(start: tuple[int, int], goal: tuple[int, int], start_minute: int = 0) -> int:
    original_up_blizzards = {
        (row, col) for row, line in enumerate(lines[1:-1]) for col, char in enumerate(line[1:-1]) if char == "^"
    }
    original_right_blizzards = {
        (row, col) for row, line in enumerate(lines[1:-1]) for col, char in enumerate(line[1:-1]) if char == ">"
    }
    original_left_blizzards = {
        (row, col) for row, line in enumerate(lines[1:-1]) for col, char in enumerate(line[1:-1]) if char == "<"
    }
    original_down_blizzards = {
        (row, col) for row, line in enumerate(lines[1:-1]) for col, char in enumerate(line[1:-1]) if char == "v"
    }
    width, height = len(lines[0]) - 2, len(lines) - 2

    @cache
    def blizzard_positions_at_minute(minute: int) -> set[tuple[int, int]]:
        up_blizzards = {((row - minute - start_minute) % height, col) for row, col in original_up_blizzards}
        down_blizzards = {((row + minute + start_minute) % height, col) for row, col in original_down_blizzards}
        left_blizzards = {(row, (col - minute - start_minute) % width) for row, col in original_left_blizzards}
        right_blizzards = {(row, (col + minute + start_minute) % width) for row, col in original_right_blizzards}
        return up_blizzards | down_blizzards | left_blizzards | right_blizzards

    open_set = [(0, (0, *start))]
    g_score: defaultdict[tuple[int, int, int], int] = defaultdict(lambda: 10**12)
    g_score[0, *start] = 0
    f_score: defaultdict[tuple[int, int, int], int] = defaultdict(lambda: 10**12)
    f_score[0, *start] = abs(goal[0] - start[0]) + abs(goal[1] - start[1])

    while open_set:
        _, (time, row, col) = heapq.heappop(open_set)
        if (row, col) == goal:
            return g_score[time, row, col]
        current_g_score = g_score[time, row, col]
        new_blizzard_positions = blizzard_positions_at_minute(time + 1)
        for drow, dcol in ((-1, 0), (0, -1), (0, 1), (1, 0), (0, 0)):
            new_row, new_col = row + drow, col + dcol
            if (
                0 <= new_col < width
                and (0 <= new_row < height or (new_row, new_col) in ((-1, 0), (height, width - 1)))
                and (new_row, new_col) not in new_blizzard_positions
            ):
                tentative_g_score = current_g_score + 1
                if tentative_g_score < g_score[time + 1, new_row, new_col]:
                    g_score[time + 1, new_row, new_col] = tentative_g_score
                    f_score[time + 1, new_row, new_col] = (
                        tentative_g_score + abs(goal[0] - new_row) + abs(goal[1] - new_col)
                    )
                    heapq.heappush(open_set, (f_score[time + 1, new_row, new_col], (time + 1, new_row, new_col)))
    raise ValueError("failed to find path")


def part_1() -> None:
    width, height = len(lines[0]) - 2, len(lines) - 2
    print(a_star((-1, 0), (height, width - 1)))


def part_2() -> None:
    width, height = len(lines[0]) - 2, len(lines) - 2
    first_trip_time = a_star((-1, 0), (height, width - 1))
    return_trup_time = a_star((height, width - 1), (-1, 0), start_minute=first_trip_time)
    second_trip_time = a_star((-1, 0), (height, width - 1), start_minute=first_trip_time + return_trup_time)
    print(first_trip_time + return_trup_time + second_trip_time)
