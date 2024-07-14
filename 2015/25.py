from typing import cast

import numpy as np
import numpy.typing as npt


def get_code(row: int, col: int) -> int:
    diagonal = row + col - 1
    row -= 1
    col -= 1
    codes = cast(npt.NDArray[np.int_], np.zeros((diagonal, diagonal), dtype=int))
    codes[0, 0] = 20151125

    for d in range(1, diagonal):
        codes[d, 0] = codes[0, d - 1] * 252533 % 33554393
        for i in range(1, d + 1):
            codes[d - i, i] = codes[d - i + 1, i - 1] * 252533 % 33554393
    return cast(int, codes[row, col])


def problem_1() -> None:
    print(get_code(2978, 3083))
