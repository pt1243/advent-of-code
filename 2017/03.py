from math import ceil, sqrt
import numpy as np


with open("./2017/resources/3.txt") as f:
    number = int(f.read().strip())


def problem_1() -> None:
    n = ceil(sqrt(number))
    if n % 2 == 0:
        n += 1
    bottom_left = n * n - n + 1
    top_left = bottom_left - n + 1
    top_right = top_left - n + 1

    bottom_middle = bottom_left + n // 2
    left_middle = top_left + n // 2
    top_middle = top_right + n // 2
    right_middle = top_right - n // 2

    if number <= top_right:
        mid_distance = abs(number - right_middle)
    elif number <= top_left:
        mid_distance = abs(number - top_middle)
    elif number <= bottom_left:
        mid_distance = abs(number - left_middle)
    else:
        mid_distance = abs(number - bottom_middle)
    print(mid_distance + n // 2)


def problem_2() -> None:
    grid_size = 20
    grid = np.zeros((grid_size + 1, grid_size + 1), dtype=int)
    zero_y, zero_x = grid_size // 2, grid_size // 2
    grid[zero_y, zero_x] = 1

    for i in range(1, grid_size // 2):
        square_size = 2 * i + 1
        for j in range(square_size - 1):
            idx_y = zero_y + i - 1 - j
            idx_x = zero_x + i
            value = np.sum(grid[idx_y - 1 : idx_y + 2, idx_x - 1 : idx_x + 2])
            if value > number:
                print(value)
                return
            grid[idx_y, idx_x] = value
        for j in range(square_size - 1):
            idx_y = zero_y - i
            idx_x = zero_x + i - 1 - j
            value = np.sum(grid[idx_y - 1 : idx_y + 2, idx_x - 1 : idx_x + 2])
            if value > number:
                print(value)
                return
            grid[idx_y, idx_x] = value
        for j in range(square_size - 1):
            idx_y = zero_y - i + 1 + j
            idx_x = zero_x - i
            value = np.sum(grid[idx_y - 1 : idx_y + 2, idx_x - 1 : idx_x + 2])
            if value > number:
                print(value)
                return
            grid[idx_y, idx_x] = value
        for j in range(square_size - 1):
            idx_y = zero_y + i
            idx_x = zero_x - i + 1 + j
            value = np.sum(grid[idx_y - 1 : idx_y + 2, idx_x - 1 : idx_x + 2])
            if value > number:
                print(value)
                return
            grid[idx_y, idx_x] = value
