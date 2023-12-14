from itertools import count, chain
from typing import Literal
import numpy as np


with open('./2023/resources/14.txt') as f:
    lines = [line.strip() for line in f]


lines_test = [
    "O....#....",
    "O.OO#....#",
    ".....##...",
    "OO.#O....O",
    ".O.....O#.",
    "O.#..O.#.#",
    "..O..#O..O",
    ".......O..",
    "#....###..",
    "#OO..#....",
]


def tilt(arr: np.ndarray, direction: Literal["N", "E", "S", "W"]) -> None:
    height, width = arr.shape
    if direction == "N" or direction == "S":
        lower_bound = 1 if direction == "N" else 0
        upper_bound = height - 1 if direction == "S" else height
        drow = -1 if direction == "N" else 1
        for col in range(width):
            while True:
                moved = False
                for row in range(lower_bound, upper_bound):
                    if arr[row, col] == 2 and arr[row + drow, col] == 0:
                        arr[row, col], arr[row + drow, col] = arr[row + drow, col], arr[row, col]
                        moved = True
                if not moved:
                    break
    else:
        lower_bound = 1 if direction == "W" else 0
        upper_bound = width - 1 if direction == "E" else width
        dcol = -1 if direction == "W" else 1
        for row in range(height):
            while True:
                moved = False
                for col in range(lower_bound, upper_bound):
                    if arr[row, col] == 2 and arr[row, col + dcol] == 0:
                        arr[row, col], arr[row, col + dcol] = arr[row, col + dcol], arr[row, col]
                        moved = True
                if not moved:
                    break


def problem_1() -> None:
    width = len(lines[0])
    height = len(lines)
    arr = np.zeros((height, width), dtype=int)
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == "#":
                arr[row, col] = 1
            elif char == "O":
                arr[row, col] = 2
    
    tilt(arr, "N")

    total_weight = 0
    for i, row in enumerate(arr):
        total_weight += (height - i) * np.sum(row == 2)
    print(total_weight)


def problem_2() -> None:
    seen: dict[int, np.ndarray] = {}
    width = len(lines[0])
    height = len(lines)
    arr = np.zeros((height, width), dtype=int)
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == "#":
                arr[row, col] = 1
            elif char == "O":
                arr[row, col] = 2
    
    found = False
    for i in count(1):
        tilt(arr, "N")
        tilt(arr, "W")
        tilt(arr, "S")
        tilt(arr, "E")
        for j, other_arr in seen.items():
            if np.all(arr == other_arr):
                print(f"{i = }, {j = }")
                found = True
                break
        if found:
            break
        seen[i] = arr.copy()
    cycle_length = i - j
    cycle_start = j
    final_index = cycle_start + (1_000_000_000 - cycle_start) % cycle_length
    
    total_weight = 0
    for i, row in enumerate(seen[final_index]):
        total_weight += (height - i) * np.sum(row == 2)
    print(total_weight)
