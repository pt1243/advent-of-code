import numpy as np


with open("./2024/resources/13.txt") as f:
    text = f.read().strip()


def get_cost(x1: int, x2: int, y1: int, y2: int, target_x: int, target_y: int) -> int:
    matrix = np.array([[x1, y1], [x2, y2]])
    inv = np.linalg.inv(matrix)
    a, b = np.round(np.array([target_x, target_y]).T @ inv).astype(int)
    if a * x1 + b * x2 == target_x and a * y1 + b * y2 == target_y:
        return 3 * a + b
    return 0


def problem_1() -> None:
    total = 0
    for block in text.split("\n\n"):
        lines = block.split("\n")
        x1, y1 = (int(x[2:]) for x in lines[0].split(": ")[1].split(", "))
        x2, y2 = (int(x[2:]) for x in lines[1].split(": ")[1].split(", "))
        target_x, target_y = (int(x[2:]) for x in lines[2].split(": ")[1].split(", "))

        total += get_cost(x1, x2, y1, y2, target_x, target_y)

    print(total)


def problem_2() -> None:
    total = 0
    for block in text.split("\n\n"):
        lines = block.split("\n")
        x1, y1 = (int(x[2:]) for x in lines[0].split(": ")[1].split(", "))
        x2, y2 = (int(x[2:]) for x in lines[1].split(": ")[1].split(", "))
        target_x, target_y = (int(x[2:]) for x in lines[2].split(": ")[1].split(", "))
        target_x += 10000000000000
        target_y += 10000000000000

        total += get_cost(x1, x2, y1, y2, target_x, target_y)

    print(total)
