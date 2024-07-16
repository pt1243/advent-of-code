from collections import deque

import numpy as np
import numpy.typing as npt


with open("./2016/resources/8.txt") as f:
    lines = [line.strip() for line in f]


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
    text: list[list[None | str]] = [[None for _ in range(10)] for _ in range(6)]
    for letter_idx, letter in enumerate(letters):
        for row_idx, row in enumerate(letter):
            text[row_idx][letter_idx] = "".join("■" if c else " " for c in row)
    for row in text:
        print("    ".join(char_string for char_string in row))
