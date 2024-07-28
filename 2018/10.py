import numpy as np


with open("./2018/resources/10.txt") as f:
    lines = [line.strip() for line in f]


def problem_1() -> None:
    positions = np.empty((len(lines), 2), dtype=int)
    velocities = np.empty((len(lines), 2), dtype=int)
    for i, line in enumerate(lines):
        position = line[line.index("<") + 1 : line.index(">")].split(", ")
        positions[i, :] = np.array([int(position[0].strip()), int(position[1].strip())])
        velocity = line[line.rindex("<") + 1 : line.rindex(">")].split(", ")
        velocities[i, :] = np.array([int(velocity[0].strip()), int(velocity[1].strip())])

    approx_time = int(np.mean(-positions / velocities))
    best_time, min_height = 0, float("inf")
    for t in range(approx_time - 50, approx_time + 51):
        future_position = positions + t * velocities
        height = np.max(future_position[:, 1], axis=0) - np.min(future_position[:, 1], axis=0)
        if height < min_height:
            best_time, min_height = t, height

    best_future_positions = positions + best_time * velocities
    best_future_positions -= np.min(best_future_positions, axis=0)
    output_strings = [[" " for _ in range(np.max(best_future_positions[:, 0]) + 1)] for _ in range(int(min_height) + 1)]
    for col, row in best_future_positions:
        output_strings[row][col] = "■"
    for row in output_strings:
        print("".join(row))


def problem_2() -> None:
    positions = np.empty((len(lines), 2), dtype=int)
    velocities = np.empty((len(lines), 2), dtype=int)
    for i, line in enumerate(lines):
        position = line[line.index("<") + 1 : line.index(">")].split(", ")
        positions[i, :] = np.array([int(position[0].strip()), int(position[1].strip())])
        velocity = line[line.rindex("<") + 1 : line.rindex(">")].split(", ")
        velocities[i, :] = np.array([int(velocity[0].strip()), int(velocity[1].strip())])

    approx_time = int(np.mean(-positions / velocities))
    best_time, min_height = 0, float("inf")
    for t in range(approx_time - 50, approx_time + 51):
        future_position = positions + t * velocities
        height = np.max(future_position[:, 1], axis=0) - np.min(future_position[:, 1], axis=0)
        if height < min_height:
            best_time, min_height = t, height
    print(best_time)
