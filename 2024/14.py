import re
from dataclasses import dataclass
from itertools import count
from math import prod
from statistics import stdev

with open("./2024/resources/14.txt") as f:
    lines = f.read().splitlines()


@dataclass
class Robot:
    px: int
    py: int
    vx: int
    vy: int


def problem_1() -> None:
    width, height = 101, 103
    quadrants = [0, 0, 0, 0]
    for line in lines:
        px, py, vx, vy = map(int, re.findall(r"-?\d+", line))
        final_x = (px + 100 * vx) % width
        final_y = (py + 100 * vy) % height
        if final_x <= width // 2 - 1:
            if final_y <= height // 2 - 1:
                quadrants[0] += 1
            if final_y >= height // 2 + 1:
                quadrants[1] += 1
        if final_x >= width // 2 + 1:
            if final_y <= height // 2 - 1:
                quadrants[2] += 1
            if final_y >= height // 2 + 1:
                quadrants[3] += 1
    print(prod(quadrants))


def problem_2() -> None:
    width, height = 101, 103
    robots = [Robot(*map(int, re.findall(r"-?\d+", line))) for line in lines]
    for i in count(1):
        for robot in robots:
            robot.px += robot.vx
            robot.px %= width
            robot.py += robot.vy
            robot.py %= height
        if stdev(robot.py for robot in robots) < 25 and stdev(robot.px for robot in robots) < 25:
            print(i)
            break
