import numpy as np


def get_code(row: int, col: int) -> int:
    diagonal = row + col - 1
    row -= 1
    col -= 1
    codes = np.zeros((diagonal, diagonal), dtype=np.int64)
    codes[0, 0] = 20151125

    for d in range(1, diagonal):
        codes[d, 0] = codes[0, d-1] * 252533 % 33554393
        for i in range(1, d+1):
            codes[d-i, i] = codes[d-i+1, i-1] * 252533 % 33554393
    print(codes[row, col])
    

def problem_1():
    get_code(2978, 3083)