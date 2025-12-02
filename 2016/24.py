import heapq
from collections import defaultdict
from collections.abc import Iterator
from itertools import combinations

with open("./2016/resources/24.txt") as f:
    lines = f.read().splitlines()


def find_distance(start_pos: tuple[int, int], end_pos: tuple[int, int]) -> set[tuple[int, int]]:
    def h(pos: tuple[int, int]) -> int:
        return abs(end_pos[0] - pos[0]) + abs(end_pos[1] - pos[1])

    def get_neighbours(pos: tuple[int, int]) -> Iterator[tuple[int, int]]:
        for drow, dcol in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if lines[pos[0] + drow][pos[1] + dcol] != "#":
                yield pos[0] + drow, pos[1] + dcol

    open_set = [(h(start_pos), start_pos)]
    open_set_set = {start_pos}
    came_from: dict[tuple[int, int], tuple[int, int]] = {}
    g_score: defaultdict[tuple[int, int], int] = defaultdict(lambda: 10**12)
    g_score[start_pos] = 0
    f_score: defaultdict[tuple[int, int], int] = defaultdict(lambda: 10**12)
    f_score[start_pos] = h(start_pos)

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == end_pos:
            total_path = {current}
            while current in came_from.keys():
                current = came_from[current]
                total_path.add(current)
            return total_path
        open_set_set.remove(current)
        for neighbour in get_neighbours(current):
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = tentative_g_score
                f_score[neighbour] = tentative_g_score + h(neighbour)
                if neighbour not in open_set_set:
                    open_set_set.add(neighbour)
                    neighbour_item = (f_score[neighbour], neighbour)
                    heapq.heappush(open_set, neighbour_item)
    return set()


def part_1() -> None:
    digits = {char: (i, j) for i, row in enumerate(lines) for j, char in enumerate(row) if char.isnumeric()}
    connections = defaultdict(list)

    for start_digit, end_digit in combinations(digits.keys(), 2):
        start_pos, end_pos = digits[start_digit], digits[end_digit]
        path = find_distance(start_pos, end_pos)
        found_other_digit = False
        for digit, digit_pos in digits.items():
            if digit == start_digit or digit == end_digit:
                continue
            if digit_pos in path:
                found_other_digit = True
                break
        if not found_other_digit:
            connections[start_digit].append((end_digit, len(path) - 1))
            connections[end_digit].append((start_digit, len(path) - 1))

    all_digits = set(digits.keys())
    queue = [(0, ["0"])]
    while queue:
        steps, digit_path = heapq.heappop(queue)
        if set(digit_path) == all_digits:
            print(steps)
            return
        last_digit = digit_path[-1]
        for next_digit, distance in connections[last_digit]:
            heapq.heappush(queue, (steps + distance, digit_path + [next_digit]))


def part_2() -> None:
    digits = {char: (i, j) for i, row in enumerate(lines) for j, char in enumerate(row) if char.isnumeric()}
    connections = defaultdict(list)

    for start_digit, end_digit in combinations(digits.keys(), 2):
        start_pos, end_pos = digits[start_digit], digits[end_digit]
        path = find_distance(start_pos, end_pos)
        found_other_digit = False
        for digit, digit_pos in digits.items():
            if digit == start_digit or digit == end_digit:
                continue
            if digit_pos in path:
                found_other_digit = True
                break
        if not found_other_digit:
            connections[start_digit].append((end_digit, len(path) - 1))
            connections[end_digit].append((start_digit, len(path) - 1))

    distance_to_zero = {}
    for start_digit, start_pos in digits.items():
        if start_digit == "0":
            continue
        path = find_distance(start_pos, digits["0"])
        distance_to_zero[start_digit] = len(path) - 1

    all_digits = set(digits.keys())
    queue = [(0, ["0"])]
    while queue:
        steps, digit_path = heapq.heappop(queue)
        if set(digit_path) == all_digits:
            if digit_path[-1] == "0":
                print(steps)
                return
            else:
                heapq.heappush(queue, (steps + distance_to_zero[digit_path[-1]], digit_path + ["0"]))
                continue
        last_digit = digit_path[-1]
        # optimisation: if we have gone from A -> B -> A, no need to go back to B
        digit_to_ignore = digit_path[-2] if len(digit_path) >= 3 and digit_path[-3] == digit_path[-1] else None
        for next_digit, distance in connections[last_digit]:
            if next_digit == digit_to_ignore:
                continue
            heapq.heappush(queue, (steps + distance, digit_path + [next_digit]))
