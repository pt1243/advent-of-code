import numpy as np


with open("./2018/resources/18.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    size = len(lines)
    area = np.empty((size, size), dtype=int)
    for row_idx, line in enumerate(lines):
        for col_idx, char in enumerate(line):
            if char == ".":  # open ground
                area[row_idx, col_idx] = 0
            elif char == "|":  # trees
                area[row_idx, col_idx] = 1
            else:  # lumberyard
                area[row_idx, col_idx] = 2

    full_indices = np.ones((3, 3), dtype=bool)
    full_indices[1, 1] = False
    for _ in range(10):
        new_area = np.empty_like(area)
        for i in range(size):
            for j in range(size):
                neighbours = area[max(0, i - 1) : min(size - 1, i + 1) + 1, max(0, j - 1) : min(size - 1, j + 1) + 1]
                lower_x = 1 if i == 0 else 0
                upper_x = 1 if i == size - 1 else 2
                lower_y = 1 if j == 0 else 0
                upper_y = 1 if j == size - 1 else 2
                indices = full_indices[lower_x : upper_x + 1, lower_y : upper_y + 1]
                flat_neighbours = neighbours[indices]
                item = area[i, j]
                if item == 0:
                    new_area[i, j] = 1 if np.count_nonzero(flat_neighbours == 1) >= 3 else 0
                elif item == 1:
                    new_area[i, j] = 2 if np.count_nonzero(flat_neighbours == 2) >= 3 else 1
                else:
                    new_area[i, j] = (
                        2
                        if np.count_nonzero(flat_neighbours == 1) >= 1 and np.count_nonzero(flat_neighbours == 2) >= 1
                        else 0
                    )
        area = new_area

    print(np.count_nonzero(area == 1) * np.count_nonzero(area == 2))


def problem_2() -> None:
    size = len(lines)
    area = np.empty((size, size), dtype=int)
    for row_idx, line in enumerate(lines):
        for col_idx, char in enumerate(line):
            if char == ".":  # open ground
                area[row_idx, col_idx] = 0
            elif char == "|":  # trees
                area[row_idx, col_idx] = 1
            else:  # lumberyard
                area[row_idx, col_idx] = 2

    full_indices = np.ones((3, 3), dtype=bool)
    full_indices[1, 1] = False
    previously_seen_areas = [area]
    while True:
        new_area = np.empty_like(area)
        for i in range(size):
            for j in range(size):
                neighbours = area[max(0, i - 1) : min(size - 1, i + 1) + 1, max(0, j - 1) : min(size - 1, j + 1) + 1]
                lower_x = 1 if i == 0 else 0
                upper_x = 1 if i == size - 1 else 2
                lower_y = 1 if j == 0 else 0
                upper_y = 1 if j == size - 1 else 2
                indices = full_indices[lower_x : upper_x + 1, lower_y : upper_y + 1]
                flat_neighbours = neighbours[indices]
                item = area[i, j]
                if item == 0:
                    new_area[i, j] = 1 if np.count_nonzero(flat_neighbours == 1) >= 3 else 0
                elif item == 1:
                    new_area[i, j] = 2 if np.count_nonzero(flat_neighbours == 2) >= 3 else 1
                else:
                    new_area[i, j] = (
                        2
                        if np.count_nonzero(flat_neighbours == 1) >= 1 and np.count_nonzero(flat_neighbours == 2) >= 1
                        else 0
                    )
        area = new_area

        for idx, previous_area in enumerate(previously_seen_areas):
            if np.all(previous_area == area):
                cycle_length = len(previously_seen_areas) - idx
                num_before = idx
                index_to_evaluate = (1_000_000_000 - num_before) % cycle_length + idx
                area_to_evaluate = previously_seen_areas[index_to_evaluate]
                print(np.count_nonzero(area_to_evaluate == 1) * np.count_nonzero(area_to_evaluate == 2))
                return
        previously_seen_areas.append(area)
