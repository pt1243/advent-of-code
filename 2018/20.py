import heapq
from collections import defaultdict
from typing import Mapping

with open("./2018/resources/20.txt") as f:
    full_regex = f.read().strip()


def get_doors(regex: str) -> dict[tuple[int, int], set[tuple[int, int]]]:
    doors: defaultdict[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)
    directions = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}
    current_positions = {(0, 0)}
    group_starting_positions: list[set[tuple[int, int]]] = []
    group_ending_positions: list[set[tuple[int, int]]] = []

    for char in regex.lstrip("^").rstrip("$"):
        if char == "(":
            # make a note of all the current positions; when we hit a branch, we'll start from here again
            group_starting_positions.append(current_positions)
            # make a new empty set of the ending positions; every time we finish a branch, we'll update this with all
            # our reachable positions from that branch
            group_ending_positions.append(set())
        elif char == "|":
            # add all current positions to the group ending positions
            group_ending_positions[-1].update(current_positions)
            # restart the current positions to the start of the group
            current_positions = group_starting_positions[-1]
        elif char == ")":
            # add all current positions to the group ending positions
            group_ending_positions[-1].update(current_positions)
            # after ending the group, the current positions should be the result from the group
            current_positions = group_ending_positions.pop()
            # the group starting positions now need to go back to the previous group
            group_starting_positions.pop()
        else:
            drow, dcol = directions[char]
            new_positions = set()
            for row, col in current_positions:
                new_row, new_col = row + drow, col + dcol
                doors[row, col].add((new_row, new_col))
                doors[new_row, new_col].add((row, col))
                new_positions.add((new_row, new_col))
            current_positions = new_positions
    return doors


def a_star(target: tuple[int, int], doors: Mapping[tuple[int, int], set[tuple[int, int]]]) -> int:
    start = (0, 0)
    open_set = [(0, start)]
    g_score = defaultdict(lambda: 10**12)
    g_score[start] = 0
    f_score = defaultdict(lambda: 10**12)
    f_score[start] = abs(target[0]) + abs(target[1])
    came_from: dict[tuple[int, int], tuple[int, int]] = {}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == target:
            return g_score[current]
        current_g_score = g_score[current]
        for neighbour in doors[current]:
            tentative_g_score = current_g_score + 1
            if tentative_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = tentative_g_score
                f_score[neighbour] = tentative_g_score + abs(neighbour[0] - target[0]) + abs(neighbour[1] - target[1])
                heapq.heappush(open_set, (f_score[neighbour], neighbour))
    raise ValueError("could not find path to specified target")


def part_1() -> None:
    doors = get_doors(full_regex)
    distances = [a_star(pos, doors) for pos in doors]
    print(max(distances))


def part_2() -> None:
    doors = get_doors(full_regex)
    distances = [a_star(pos, doors) for pos in doors]
    print(sum(1 for d in distances if d >= 1000))
