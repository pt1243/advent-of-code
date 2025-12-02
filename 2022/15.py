import re
from itertools import permutations
from typing import NamedTuple

with open("./2022/resources/15.txt") as f:
    lines = f.read().splitlines()


class Sensor(NamedTuple):
    x: int
    y: int
    dist: int


def part_1() -> None:
    cannot_contain_beacon: set[int] = set()
    for line in lines:
        sensor_x, sensor_y, beacon_x, beacon_y = map(int, re.findall(r"-?\d+", line))
        dist = abs(beacon_x - sensor_x) + abs(beacon_y - sensor_y)
        row_dist = abs(2000000 - sensor_y)
        cannot_contain_beacon |= set(range(sensor_x - (dist - row_dist), sensor_x + (dist - row_dist)))
    print(len(cannot_contain_beacon))


def part_2() -> None:
    sensors: list[Sensor] = []
    for line in lines:
        sensor_x, sensor_y, beacon_x, beacon_y = map(int, re.findall(r"-?\d+", line))
        sensors.append(Sensor(sensor_x, sensor_y, abs(beacon_x - sensor_x) + abs(beacon_y - sensor_y)))

    s1, s2 = next(
        (s1, s2)
        for s1, s2 in permutations(sensors, 2)
        if s1.x < s2.x and s1.y < s2.y and 0 < s2.x - s1.x + s2.y - s1.y - s1.dist - s2.dist <= 2
    )
    s3, s4 = next(
        (s3, s4)
        for s3, s4 in permutations(sensors, 2)
        if s3.x > s4.x and s3.y < s4.y and 0 < s3.x - s4.x + s4.y - s3.y - s3.dist - s4.dist <= 2
    )

    # approximate solution
    y = (-s3.x + s3.y + s3.dist + 1 + s1.x + s1.y + s1.dist + 1) // 2
    x = s1.x + s1.y + s1.dist + 1 - y

    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if (
                (x + dx - s1.x) + (y + dy - s1.y) > s1.dist
                and (s2.x - x - dx) + (s2.y - y - dy) > s2.dist
                and (s3.x - x - dx) + (y + dy - s3.y) > s3.dist
                and (x + dx - s4.x) + (s4.y - y - dy) > s4.dist
            ):
                print(4000000 * (x + dy) + (y + dy))
                return
