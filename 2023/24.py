from itertools import combinations
from typing import NamedTuple

import numpy as np


with open("./2023/resources/24.txt") as f:
    input_text = f.read().splitlines()


class Hailstone(NamedTuple):
    px: int
    py: int
    pz: int
    vx: int
    vy: int
    vz: int


def problem_1() -> None:
    hailstones: list[Hailstone] = []
    for line_text in input_text:
        pos, vel = line_text.split(" @ ")
        px, py, pz = (int(x) for x in pos.split(", "))
        vx, vy, vz = (int(x) for x in vel.split(", "))
        hailstones.append(Hailstone(px, py, pz, vx, vy, vz))

    num_intersections = 0
    lower, upper = 200000000000000, 400000000000000
    for h1, h2 in combinations(hailstones, 2):
        x1, y1, _, vx1, vy1, _ = h1
        x2, y2 = x1 + vx1, y1 + vy1
        x3, y3, _, vx2, vy2, _ = h2
        x4, y4 = x3 + vx2, y3 + vy2
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denom != 0:
            x_intersect = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
            y_intersect = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom
            if lower <= x_intersect <= upper and lower <= y_intersect <= upper:
                t1 = (x_intersect - x1) / vx1
                t2 = (x_intersect - x3) / vx2
                if t1 >= 0 and t2 >= 0:
                    num_intersections += 1
    print(num_intersections)


def problem_2() -> None:
    hailstones: list[Hailstone] = []
    for line_text in input_text:
        pos, vel = line_text.split(" @ ")
        px, py, pz = (int(x) for x in pos.split(", "))
        vx, vy, vz = (int(x) for x in vel.split(", "))
        hailstones.append(Hailstone(px, py, pz, vx, vy, vz))

    px1, py1, pz1, vx1, vy1, vz1 = hailstones[0]
    px2, py2, pz2, vx2, vy2, vz2 = hailstones[1]
    px3, py3, pz3, vx3, vy3, vz3 = hailstones[2]

    A = np.array(
        [
            [vy2 - vy1, vx1 - vx2, 0, py1 - py2, px2 - px1, 0],
            [vy3 - vy1, vx1 - vx3, 0, py1 - py3, px3 - px1, 0],
            [vz2 - vz1, 0, vx1 - vx2, pz1 - pz2, 0, px2 - px1],
            [vz3 - vz1, 0, vx1 - vx3, pz1 - pz3, 0, px3 - px1],
            [0, vz2 - vz1, vy1 - vy2, 0, pz1 - pz2, py2 - py1],
            [0, vz3 - vz1, vy1 - vy3, 0, pz1 - pz3, py3 - py1],
        ]
    )
    B = np.array(
        [
            px1 * vy1 - py1 * vx1 + py2 * vx2 - px2 * vy2,
            px1 * vy1 - py1 * vx1 + py3 * vx3 - px3 * vy3,
            px1 * vz1 - pz1 * vx1 + pz2 * vx2 - px2 * vz2,
            px1 * vz1 - pz1 * vx1 + pz3 * vx3 - px3 * vz3,
            py1 * vz1 - pz1 * vy1 + pz2 * vy2 - py2 * vz2,
            py1 * vz1 - pz1 * vy1 + pz3 * vy3 - py3 * vz3,
        ]
    ).T
    prx, pry, prz, *_ = np.linalg.solve(A, B)
    print(-1 * (round(prx) + round(pry) + round(prz)))  # unsure where the sign error is
