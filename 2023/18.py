from itertools import pairwise
from typing import Sequence


with open("./2023/resources/18.txt") as f:
    lines = [line.strip() for line in f]


def get_area(vertices: Sequence[tuple[int, int]]) -> int:
    # https://en.wikipedia.org/wiki/Shoelace_formula
    area: float = 0
    for (x1, y1), (x2, y2) in pairwise(vertices):
        area += (x1 * y2 - x2 * y1) / 2
    area = abs(area)
    for (x1, y1), (x2, y2) in pairwise(vertices):
        area += (abs(x2 - x1) + abs(y2 - y1)) / 2
    return int(area) + 1


def problem_1() -> None:
    vertices = [(0, 0)]
    directions = {"U": (0, 1), "D": (0, -1), "L": (-1, 0), "R": (1, 0)}
    for line in lines:
        direction, dist_str = line.split()[:2]
        x, y = vertices[-1]
        dx, dy = directions[direction]
        dist = int(dist_str)
        new_x, new_y = x + dist * dx, y + dist * dy
        vertices.append((new_x, new_y))
    print(get_area(vertices))


def problem_2() -> None:
    vertices = [(0, 0)]
    directions = {"3": (0, 1), "1": (0, -1), "2": (-1, 0), "0": (1, 0)}
    for line in lines:
        hex_part = line.split()[-1]
        dist = int(hex_part[2:7], 16)
        x, y = vertices[-1]
        dx, dy = directions[hex_part[7]]
        new_x, new_y = x + dist * dx, y + dist * dy
        vertices.append((new_x, new_y))
    print(get_area(vertices))
