import numpy as np


with open("./2018/resources/11.txt") as f:
    grid_serial_number = int(f.read().strip())


def problem_1() -> None:
    power_levels = np.empty((300, 300), dtype=int)
    for i in range(300):
        for j in range(300):
            x = i + 1
            y = j + 1
            rack_id = x + 10
            power_level = rack_id * y
            power_level += grid_serial_number
            power_level *= rack_id
            power_level = (power_level % 1000) // 100
            power_level -= 5
            power_levels[i, j] = power_level
    max_power_level = 0
    x, y = 0, 0
    for i in range(298):
        for j in range(298):
            power_level = np.sum(power_levels[i : i + 3, j : j + 3])
            if power_level > max_power_level:
                max_power_level = power_level
                x, y = i + 1, j + 1
    print(f"{x},{y}")


def problem_2() -> None:
    power_levels = np.empty((300, 300), dtype=int)
    for i in range(300):
        for j in range(300):
            x = i + 1
            y = j + 1
            rack_id = x + 10
            power_level = rack_id * y
            power_level += grid_serial_number
            power_level *= rack_id
            power_level = (power_level % 1000) // 100
            power_level -= 5
            power_levels[i, j] = power_level
    max_power_level = 0
    x, y, optimal_size = 0, 0, 0
    for size in range(1, 301):
        for i in range(301 - size):
            for j in range(301 - size):
                power_level = np.sum(power_levels[i : i + size, j : j + size])
                if power_level > max_power_level:
                    max_power_level = power_level
                    x, y, optimal_size = i + 1, j + 1, size
    print(f"{x},{y},{optimal_size}")
