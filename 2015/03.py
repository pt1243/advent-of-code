from collections import defaultdict
from itertools import batched

with open("./2015/resources/3.txt") as f:
    directions = f.read().strip()


def problem_1() -> None:
    houses = defaultdict(int)
    houses[0, 0] = 1
    current_x, current_y = 0, 0
    lookup = {"^": (0, 1), "v": (0, -1), ">": (1, 0), "<": (-1, 0)}
    for direction in directions:
        dx, dy = lookup[direction]
        current_x += dx
        current_y += dy
        houses[current_x, current_y] += 1
    print(len(houses))


def problem_2() -> None:
    houses = defaultdict(int)
    houses[(0, 0)] = 1
    santa_x, santa_y = 0, 0
    robo_santa_x, robo_santa_y = 0, 0
    lookup = {"^": (0, 1), "v": (0, -1), ">": (1, 0), "<": (-1, 0)}
    for santa_direction, robo_santa_direction in batched(directions, 2):
        santa_dx, santa_dy = lookup[santa_direction]
        santa_x += santa_dx
        santa_y += santa_dy
        robo_santa_dx, robo_santa_dy = lookup[robo_santa_direction]
        robo_santa_x += robo_santa_dx
        robo_santa_y += robo_santa_dy

        houses[santa_x, santa_y] += 1
        houses[robo_santa_x, robo_santa_y] += 1
    print(len(houses))
