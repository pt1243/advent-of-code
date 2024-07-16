from itertools import combinations
from collections import defaultdict
import heapq


with open("./2016/resources/24.txt") as f:
    lines = [line.strip() for line in f]


def find_distance(start_pos, end_pos):
    def h(pos):
        return abs(end_pos[0] - pos[0]) + abs(end_pos[1] - pos[1])
    
    def get_neighbours(pos):
        for drow, dcol in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if lines[pos[0] + drow][pos[1] + dcol] != "#":
                yield pos[0] + drow, pos[1] + dcol
    
    open_set = [(h(start_pos), start_pos)]
    open_set_set = {start_pos}
    came_from = {}
    g_score = defaultdict(lambda: float("inf"))
    g_score[start_pos] = 0
    f_score = defaultdict(lambda: float("inf"))
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
                    came_from
                    open_set_set.add(neighbour)
                    heapq.heappush(open_set, (f_score[neighbour], neighbour))


def problem_1() -> None:
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
        steps, path = heapq.heappop(queue)
        if set(path) == all_digits:
            print(steps)
            return
        last_digit = path[-1]
        for next_digit, distance in connections[last_digit]:
            heapq.heappush(queue, (steps + distance, path + [next_digit]))


def problem_2() -> None:
    # WARNING: slow (~90 s)
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
        steps, path = heapq.heappop(queue)
        if set(path) == all_digits:
            if path[-1] == "0":
                print(steps)
                return
            else:
                heapq.heappush(queue, (steps + distance_to_zero[path[-1]], path + ["0"]))
                continue
        last_digit = path[-1]
        for next_digit, distance in connections[last_digit]:
            heapq.heappush(queue, (steps + distance, path + [next_digit]))
