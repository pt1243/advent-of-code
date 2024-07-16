from functools import partial


with open("./2016/resources/2.txt") as f:
    lines = [line.strip() for line in f]


def clamp(val: int, min_val: int, max_val: int) -> int:
    return val if min_val <= val <= max_val else (min_val if val < min_val else max_val)


def problem_1() -> None:
    row, col = 1, 1
    code = ""

    for line in lines:
        for char in line:
            if char == "U":
                row -= 1
            elif char == "D":
                row += 1
            elif char == "L":
                col -= 1
            else:
                col += 1

            row = clamp(row, 0, 2)
            col = clamp(col, 0, 2)

        code += str(row * 3 + col + 1)

    print(code)


def problem_2() -> None:
    row, col = 2, 0
    code = ""

    bounds = {
        0: partial(clamp, min_val=2, max_val=2),
        1: partial(clamp, min_val=1, max_val=3),
        2: partial(clamp, min_val=0, max_val=4),
        3: partial(clamp, min_val=1, max_val=3),
        4: partial(clamp, min_val=2, max_val=2),
    }

    def keypad(row: int, col: int) -> str:
        if row == 0:
            return "1"
        if row == 1:
            return str(col + 1)
        if row == 2:
            return str(col + 5)
        if row == 3:
            return chr(64 + col)
        return "D"

    for line in lines:
        for char in line:
            if char == "U":
                row = bounds[col](row - 1)
            elif char == "D":
                row = bounds[col](row + 1)
            elif char == "L":
                col = bounds[row](col - 1)
            else:
                col = bounds[row](col + 1)

        code += keypad(row, col)

    print(code)
