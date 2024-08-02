import numpy as np


with open("./2015/resources/6.txt") as f:
    instructions = f.read().splitlines()


def problem_1() -> None:
    lights = np.zeros((1000, 1000), dtype=bool)
    for instruction in instructions:
        start_str, end_str = instruction.split(" through ")
        end_x, end_y = tuple(int(i) for i in end_str.split(","))
        start_x, start_y = tuple(int(i) for i in start_str.rsplit(" ", maxsplit=1)[1].split(","))

        subarray = lights[start_x : end_x + 1, start_y : end_y + 1]

        if instruction.startswith("turn on"):
            lights[start_x : end_x + 1, start_y : end_y + 1] = np.ones_like(subarray)
        elif instruction.startswith("turn off"):
            lights[start_x : end_x + 1, start_y : end_y + 1] = np.zeros_like(subarray)
        else:
            lights[start_x : end_x + 1, start_y : end_y + 1] = np.invert(subarray)

    print(np.sum(lights))


def problem_2() -> None:
    lights = np.zeros((1000, 1000), dtype=int)
    for instruction in instructions:
        start_str, end_str = instruction.split(" through ")
        end_x, end_y = tuple(int(i) for i in end_str.split(","))
        start_x, start_y = tuple(int(i) for i in start_str.rsplit(" ", maxsplit=1)[1].split(","))

        subarray = lights[start_x : end_x + 1, start_y : end_y + 1]

        if instruction.startswith("turn on"):
            lights[start_x : end_x + 1, start_y : end_y + 1] = subarray + 1
        elif instruction.startswith("turn off"):
            lights[start_x : end_x + 1, start_y : end_y + 1] = np.maximum(np.zeros_like(subarray), subarray - 1)
        else:
            lights[start_x : end_x + 1, start_y : end_y + 1] = subarray + 2

    print(np.sum(lights))
