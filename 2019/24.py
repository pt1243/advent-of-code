from collections import defaultdict
from itertools import chain

import numpy as np
import numpy.typing as npt

with open("./2019/resources/24.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    def array_to_tuple(arr: npt.NDArray[np.bool_]) -> tuple[tuple[int, ...], ...]:
        return tuple(chain.from_iterable(tuple(row) for row in arr))

    grid = np.array([[char == "#" for char in line] for line in lines], dtype=bool)
    seen = {array_to_tuple(grid)}
    while True:
        new_grid = grid.copy()
        for row in range(5):
            for col in range(5):
                neighbours = 0
                if row > 0 and grid[row - 1, col]:
                    neighbours += 1
                if row < 4 and grid[row + 1, col]:
                    neighbours += 1
                if col > 0 and grid[row, col - 1]:
                    neighbours += 1
                if col < 4 and grid[row, col + 1]:
                    neighbours += 1
                if grid[row, col] and neighbours != 1:
                    new_grid[row, col] = False
                elif not grid[row, col] and (neighbours == 1 or neighbours == 2):
                    new_grid[row, col] = True
        tuple_array = array_to_tuple(new_grid)
        if tuple_array in seen:
            total = 0
            for i, val in enumerate(tuple_array):
                total += val * 2**i
            print(total)
            return
        seen.add(tuple_array)
        grid = new_grid


def problem_2() -> None:
    levels: defaultdict[int, npt.NDArray[np.bool_]] = defaultdict(lambda: np.zeros((5, 5), dtype=bool))

    levels[0] = np.array([[char == "#" for char in line] for line in lines], dtype=bool)
    for _ in range(200):
        new_levels: defaultdict[int, npt.NDArray[np.bool_]] = defaultdict(lambda: np.zeros((5, 5), dtype=bool))
        keys = list(levels.keys())
        for level in keys:
            level_arr = levels[level]
            new_level_arr = new_levels[level]
            for row in range(5):
                for col in range(5):
                    if (row, col) == (2, 2):
                        continue
                    neighbours = 0
                    # outer level
                    if row == 0:
                        neighbours += levels[level - 1][1, 2]
                    elif row == 4:
                        neighbours += levels[level - 1][3, 2]
                    if col == 0:
                        neighbours += levels[level - 1][2, 1]
                    elif col == 4:
                        neighbours += levels[level - 1][2, 3]
                    # normal neighbours:
                    if row > 0 and (row, col) != (3, 2):
                        neighbours += level_arr[row - 1, col]
                    if row < 4 and (row, col) != (1, 2):
                        neighbours += level_arr[row + 1, col]
                    if col > 0 and (row, col) != (2, 3):
                        neighbours += level_arr[row, col - 1]
                    if col < 4 and (row, col) != (2, 1):
                        neighbours += level_arr[row, col + 1]
                    # inner level
                    if (row, col) == (1, 2):
                        neighbours += np.sum(levels[level + 1][0, :])
                    elif (row, col) == (2, 1):
                        neighbours += np.sum(levels[level + 1][:, 0])
                    elif (row, col) == (2, 3):
                        neighbours += np.sum(levels[level + 1][:, 4])
                    elif (row, col) == (3, 2):
                        neighbours += np.sum(levels[level + 1][4, :])

                    if not level_arr[row, col]:  # empty space becomes infested if 1 or 2 neighbours
                        if neighbours == 1 or neighbours == 2:
                            new_level_arr[row, col] = True
                    else:  # infested staays infested unless exactly one neighbour
                        if neighbours == 1:
                            new_level_arr[row, col] = True
        # process newly explored levels
        min_level = min(keys)
        min_level_arr = levels[min_level]
        new_min_level_arr = new_levels[min_level - 1]
        if np.sum(min_level_arr[0, :]) == 1 or np.sum(min_level_arr[0, :]) == 2:
            new_min_level_arr[1, 2] = True
        if np.sum(min_level_arr[4, :]) == 1 or np.sum(min_level_arr[4, :]) == 2:
            new_min_level_arr[3, 2] = True
        if np.sum(min_level_arr[:, 0]) == 1 or np.sum(min_level_arr[:, 0]) == 2:
            new_min_level_arr[2, 1] = True
        if np.sum(min_level_arr[:, 4]) == 1 or np.sum(min_level_arr[:, 4]) == 2:
            new_min_level_arr[2, 3] = True

        max_level = max(keys)
        max_level_arr = levels[max_level]
        new_max_level_arr = new_levels[max_level + 1]
        if max_level_arr[1, 2]:
            new_max_level_arr[0, :] = True
        if max_level_arr[2, 1]:
            new_max_level_arr[:, 0] = True
        if max_level_arr[2, 3]:
            new_max_level_arr[:, 4] = True
        if max_level_arr[3, 2]:
            new_max_level_arr[4, :] = True

        levels = new_levels

    print(sum(np.sum(level_arr) for level_arr in levels.values()))
