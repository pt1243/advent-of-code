from __future__ import annotations

import heapq
from collections import defaultdict
from enum import Enum, auto
from typing import Generator

import numpy as np

with open("./2018/resources/22.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    depth = int(lines[0].split(": ")[1])
    target_x, target_y = (int(x) for x in lines[1].split(": ")[1].split(","))

    geologic_index = np.empty((target_x + 1, target_y + 1), dtype=int)
    erosion_level = np.empty((target_x + 1, target_y + 1), dtype=int)

    geologic_index[0, 0] = 0
    geologic_index[target_x, target_y] = 0
    geologic_index[1:, 0] = np.arange(1, target_x + 1) * 16807
    geologic_index[0, 1:] = np.arange(1, target_y + 1) * 48271
    erosion_level[0, 0] = (geologic_index[0, 0] + depth) % 20183
    erosion_level[target_x, target_y] = (geologic_index[target_x, target_y] + depth) % 20183
    erosion_level[1:, 0] = (geologic_index[1:, 0] + depth) % 20183
    erosion_level[0, 1:] = (geologic_index[0, 1:] + depth) % 20183

    for x in range(1, target_x + 1):
        for y in range(1, target_y + 1):
            if x == target_x and y == target_y:
                continue
            geologic_index[x, y] = erosion_level[x - 1, y] * erosion_level[x, y - 1]
            erosion_level[x, y] = (geologic_index[x, y] + depth) % 20183

    print(np.sum(erosion_level % 3))


def problem_2() -> None:
    depth = int(lines[0].split(": ")[1])
    target_x, target_y = (int(x) for x in lines[1].split(": ")[1].split(","))

    extra_buffer = 20  # in case the shortest path exceeds the x and y of the target

    geologic_index = np.empty((target_x + extra_buffer + 1, target_y + extra_buffer + 1), dtype=int)
    erosion_level = np.empty((target_x + extra_buffer + 1, target_y + extra_buffer + 1), dtype=int)

    geologic_index[0, 0] = 0
    geologic_index[target_x, target_y] = 0
    geologic_index[1:, 0] = np.arange(1, target_x + extra_buffer + 1) * 16807
    geologic_index[0, 1:] = np.arange(1, target_y + extra_buffer + 1) * 48271
    erosion_level[0, 0] = (geologic_index[0, 0] + depth) % 20183
    erosion_level[target_x, target_y] = (geologic_index[target_x, target_y] + depth) % 20183
    erosion_level[1:, 0] = (geologic_index[1:, 0] + depth) % 20183
    erosion_level[0, 1:] = (geologic_index[0, 1:] + depth) % 20183

    for x in range(1, target_x + extra_buffer + 1):
        for y in range(1, target_y + extra_buffer + 1):
            if x == target_x and y == target_y:
                continue
            geologic_index[x, y] = erosion_level[x - 1, y] * erosion_level[x, y - 1]
            erosion_level[x, y] = (geologic_index[x, y] + depth) % 20183

    types = erosion_level % 3

    class Equipment(Enum):
        Neither = auto()
        Torch = auto()
        ClimbingGear = auto()

        def __lt__(self, other: object) -> bool:
            if type(other) is Equipment:
                return self.value < other.value
            return NotImplemented

    equipment_regions = {Equipment.Neither: {1, 2}, Equipment.Torch: {0, 2}, Equipment.ClimbingGear: {0, 1}}

    distances = ((-1, 0), (1, 0), (0, -1), (0, 1))

    def get_neighbour_states(
        position: tuple[int, int], equipment: Equipment
    ) -> Generator[tuple[int, tuple[int, int], Equipment], None, None]:
        # consider changing tool
        current_region = types[position[0], position[1]]
        for new_equipment in Equipment:
            if new_equipment is equipment:
                continue
            if current_region not in equipment_regions[new_equipment]:
                continue
            yield 7, position, new_equipment
        for dx, dy in distances:
            new_x, new_y = position[0] + dx, position[1] + dy
            if new_x < 0 or new_y < 0 or new_x == target_x + extra_buffer or new_y == target_y + extra_buffer:
                continue
            new_region = types[new_x, new_y]
            if new_region not in equipment_regions[equipment]:
                continue
            yield 1, (new_x, new_y), equipment

    start = ((0, 0), Equipment.Torch)
    open_set = [(0, *start)]
    g_score = defaultdict(lambda: 10**12)
    g_score[start] = 0
    f_score = defaultdict(lambda: 10**12)
    f_score[start] = target_x + target_y
    came_from = {}
    while open_set:
        _, position, equipment = heapq.heappop(open_set)
        current = (position, equipment)
        if position == (target_x, target_y) and equipment is Equipment.Torch:
            print(g_score[current])
            return
        current_g_score = g_score[current]
        for dist, new_position, new_equipment in get_neighbour_states(position, equipment):
            neighbour = (new_position, new_equipment)
            tentative_g_score = current_g_score + dist
            if tentative_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = tentative_g_score
                new_x, new_y = new_position
                f_score[neighbour] = tentative_g_score + abs(new_x - target_x) + abs(new_y - target_y)
                heapq.heappush(open_set, (f_score[neighbour], new_position, new_equipment))
