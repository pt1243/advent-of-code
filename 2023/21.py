import numpy as np


with open("./2023/resources/21.txt") as f:
    lines = [line.strip() for line in f]


def get_num_positions(steps: int) -> int:
    starting_row = [i for i, line in enumerate(lines) if "S" in line][0]
    starting_col = lines[starting_row].index("S")
    vacant = {(row, col) for row, line in enumerate(lines) for col, char in enumerate(line) if char != "#"}
    current = {(starting_row, starting_col)}
    for _ in range(steps):
        new: set[tuple[int, int]] = set()
        for row, col in current:
            if ((row - 1) % 131, col % 131) in vacant:
                new.add((row - 1, col))
            if ((row + 1) % 131, col % 131) in vacant:
                new.add((row + 1, col))
            if (row % 131, (col - 1) % 131) in vacant:
                new.add((row, col - 1))
            if (row % 131, (col + 1) % 131) in vacant:
                new.add((row, col + 1))
        current = new
    return len(current)


def problem_1() -> None:
    print(get_num_positions(64))


def problem_2() -> None:
    f0 = get_num_positions(65 + 131 * 0)
    f1 = get_num_positions(65 + 131 * 1)
    f2 = get_num_positions(65 + 131 * 2)

    coeffs = np.linalg.inv(np.array([[0, 0, 1], [1, 1, 1], [4, 2, 1]])) @ np.array([f0, f1, f2]).T
    a, b, c = (int(coeff) for coeff in coeffs)
    x = (26501365 - 65) // 131
    print(a * x**2 + b * x + c)
