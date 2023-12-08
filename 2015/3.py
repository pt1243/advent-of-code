from collections import defaultdict
from itertools import batched


with open('./2015/resources/3.txt') as f:
    directions = f.read().strip()


def problem_1() -> None:
    houses = defaultdict(int)
    houses[(0, 0)] = 1
    current_x, current_y = 0, 0
    for direction in directions:
        if direction == "^":
            current_y += 1
        elif direction == "v":
            current_y -= 1
        elif direction == ">":
            current_x += 1
        else:
            current_x -= 1

        houses[(current_x, current_y)] += 1
    print(len(houses))


def problem_2() -> None:
    houses = defaultdict(int)
    houses[(0, 0)] = 1
    santa_x, santa_y = 0, 0
    robo_santa_x, robo_santa_y = 0, 0
    for santa_direction, robo_santa_direction in batched(directions, 2):
        if santa_direction == "^":
            santa_y += 1
        elif santa_direction == "v":
            santa_y -= 1
        elif santa_direction == ">":
            santa_x += 1
        else:
            santa_x -= 1

        if robo_santa_direction == "^":
            robo_santa_y += 1
        elif robo_santa_direction == "v":
            robo_santa_y -= 1
        elif robo_santa_direction == ">":
            robo_santa_x += 1
        else:
            robo_santa_x -= 1

        houses[(santa_x, santa_y)] += 1
        houses[(robo_santa_x, robo_santa_y)] += 1
    print(len(houses))
