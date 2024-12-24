from functools import cache
from itertools import pairwise, product
from more_itertools import split_after


with open("./2024/resources/21.txt") as f:
    codes = f.read().splitlines()


@cache
def paths_between_numeric(start: str, end: str) -> list[str]:
    numeric_keypad_positions = {
        "7": (0, 0),
        "8": (0, 1),
        "9": (0, 2),
        "4": (1, 0),
        "5": (1, 1),
        "6": (1, 2),
        "1": (2, 0),
        "2": (2, 1),
        "3": (2, 2),
        "0": (3, 1),
        "A": (3, 2),
    }
    start_row, start_col = numeric_keypad_positions[start]
    end_row, end_col = numeric_keypad_positions[end]
    min_dist = abs(end_row - start_row) + abs(end_col - start_col)
    all_paths: list[str] = []
    open_set = [(start_row, start_col, "")]
    while open_set:
        row, col, path = open_set.pop()
        if row == end_row and col == end_col and len(path) == min_dist:
            all_paths.append(path + "A")
            continue
        if len(path) < min_dist:
            for (drow, dcol), direction in {(-1, 0): "^", (0, 1): ">", (1, 0): "v", (0, -1): "<"}.items():
                new_row, new_col = row + drow, col + dcol
                if 0 <= new_row <= 3 and 0 <= new_col <= 2 and (new_row, new_col) != (3, 0):
                    open_set.append((new_row, new_col, path + direction))
    return all_paths


@cache
def paths_between_directional(start: str, end: str) -> list[str]:
    directional_keypad_positions = {"^": (0, 1), "A": (0, 2), "<": (1, 0), "v": (1, 1), ">": (1, 2)}
    start_row, start_col = directional_keypad_positions[start]
    end_row, end_col = directional_keypad_positions[end]
    min_dist = abs(end_row - start_row) + abs(end_col - start_col)
    all_paths: list[str] = []
    open_set = [(start_row, start_col, "")]
    while open_set:
        row, col, path = open_set.pop()
        if row == end_row and col == end_col and len(path) == min_dist:
            all_paths.append(path + "A")
            continue
        if len(path) < min_dist:
            for (drow, dcol), direction in {(-1, 0): "^", (0, 1): ">", (1, 0): "v", (0, -1): "<"}.items():
                new_row, new_col = row + drow, col + dcol
                if 0 <= new_row <= 1 and 0 <= new_col <= 2 and (new_row, new_col) != (0, 0):
                    open_set.append((new_row, new_col, path + direction))
    return all_paths


@cache
def shortest_distance_directional(key_sequence: str, depth: int) -> int:
    if depth == 0:  # direct access, just press the keys
        return len(key_sequence)
    total = 0
    # everything returns to A eventually, so split based on that
    for subsequence_list in split_after(key_sequence, lambda key: key == "A"):
        # all possible paths is the Cartesian product of the options for going from one key to the next; note that we
        # start on A, so add that to the subsequence
        subsequence = "A" + "".join(subsequence_list)
        total += min(
            shortest_distance_directional("".join(path), depth - 1)
            for path in product(*(paths_between_directional(key_1, key_2) for key_1, key_2 in pairwise(subsequence)))
        )
    return total


def problem_1() -> None:
    total = 0
    for code in codes:
        min_keypresses = min(
            shortest_distance_directional("".join(path), 2)
            for path in product(*(paths_between_numeric(key_1, key_2) for key_1, key_2 in pairwise("A" + code)))
        )
        total += min_keypresses * int(code.replace("A", ""))
    print(total)


def problem_2() -> None:
    total = 0
    for code in codes:
        min_keypresses = min(
            shortest_distance_directional("".join(path), 25)
            for path in product(*(paths_between_numeric(key_1, key_2) for key_1, key_2 in pairwise("A" + code)))
        )
        total += min_keypresses * int(code.replace("A", ""))
    print(total)
