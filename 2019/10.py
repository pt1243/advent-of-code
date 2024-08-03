from collections import deque
from itertools import groupby
from math import atan2, pi
from operator import itemgetter


with open("./2019/resources/10.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    asteroids: list[tuple[int, int]] = []
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == "#":
                asteroids.append((row, col))
    
    most_detected = 0
    for monitoring_station in asteroids:
        angles: set[float] = set()
        for asteroid in asteroids:
            if monitoring_station == asteroid:
                continue
            y, x = monitoring_station[0] - asteroid[0], asteroid[1] - monitoring_station[1]
            angles.add(atan2(y, x))
        most_detected = max(most_detected, len(angles))
    print(most_detected)


def problem_2() -> None:
    asteroids: list[tuple[int, int]] = []
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == "#":
                asteroids.append((row, col))

    most_detected = 0
    best_location = (0, 0)
    for monitoring_station in asteroids:
        angles: set[float] = set()
        for asteroid in asteroids:
            if monitoring_station == asteroid:
                continue
            y, x = monitoring_station[0] - asteroid[0], asteroid[1] - monitoring_station[1]
            angles.add(atan2(y, x))
        if len(angles) > most_detected:
            most_detected = len(angles)
            best_location = monitoring_station

    asteroids.remove(best_location)
    all_angles: set[tuple[float, int, int, int]] = set()
    station_row, station_col = best_location
    for asteroid in asteroids:
        row, col = asteroid
        dist = (row - station_row)**2 + (col - station_col)**2
        vertical_dist = station_row - row
        horizontal_dist = col - station_col
        raw_angle = atan2(horizontal_dist, vertical_dist)
        if raw_angle < 0:
            raw_angle += 2*pi
        all_angles.add((raw_angle, dist, row, col))
    
    all_items: deque[deque[tuple[int, int]]] = deque()
    for _, g in groupby(sorted(all_angles), key=itemgetter(0)):
        sorted_by_dist = sorted(g, key=itemgetter(1))
        all_items.append(deque((item[2], item[3]) for item in sorted_by_dist))
    
    num_vapourised = 0
    while all_items:
        asteroids_at_current_angle = all_items[0]
        if not asteroids_at_current_angle:
            all_items.popleft()
            continue
        asteroid_to_vapourise = asteroids_at_current_angle.popleft()
        num_vapourised += 1
        if num_vapourised == 200:
            print(asteroid_to_vapourise[0] + asteroid_to_vapourise[1] * 100)
            return
        all_items.rotate(-1)
