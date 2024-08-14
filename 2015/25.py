import numpy as np


with open("./2015/resources/25.txt") as f:
    console_message = f.read().strip()


def problem_1() -> None:
    split = console_message.split()
    row, col = int(split[15].strip(",")), int(split[17].strip("."))

    diagonal = row + col - 1
    row -= 1
    col -= 1
    codes = np.zeros((diagonal, diagonal), dtype=int)
    codes[0, 0] = 20151125

    for d in range(1, diagonal):
        codes[d, 0] = int(codes[0, d - 1]) * 252533 % 33554393
        for i in range(1, d + 1):
            codes[d - i, i] = int(codes[d - i + 1, i - 1]) * 252533 % 33554393
    print(codes[row, col])
