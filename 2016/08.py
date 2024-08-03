from collections import deque

import numpy as np
import numpy.typing as npt


with open("./2016/resources/8.txt") as f:
    lines = f.read().splitlines()


def process_screen() -> npt.NDArray[np.bool_]:
    screen = np.zeros((6, 50), dtype=bool)

    for line in lines:
        if line.startswith("rect"):
            w, h = (int(c) for c in line.split()[1].split("x"))
            screen[:h, :w] = np.ones((h, w), dtype=bool)
        elif "row" in line:
            row_idx = int(line.split()[2].split("=")[1])
            n = int(line.split()[-1])
            row = deque(screen[row_idx, :])
            row.rotate(n)
            screen[row_idx, :] = np.array(row, dtype=bool)
        else:
            col_idx = int(line.split()[2].split("=")[1])
            n = int(line.split()[-1])
            col = deque(screen[:, col_idx])
            col.rotate(n)
            screen[:, col_idx] = np.array(col, dtype=bool)

    return screen


def problem_1() -> None:
    screen = process_screen()
    print(np.sum(screen))


def problem_2() -> None:
    screen = process_screen()
    letters = np.split(screen, 10, axis=1)
    for row in range(6):
        for letter in letters:
            print("".join("█" if char else " " for char in letter[row]), end=" ")
        print()
