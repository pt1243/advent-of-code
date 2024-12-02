from itertools import count
import numpy as np


with open("./2016/resources/20.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    ranges = sorted(tuple(int(val) for val in line.split("-")) for line in lines)
    for i in count():
        if not any(lower <= i <= upper for lower, upper in ranges):
            print(i)
            break


def problem_2() -> None:
    upper_limit = 4294967295
    arr = np.ones(upper_limit + 1, dtype=bool)
    ranges = sorted(tuple(int(val) for val in line.split("-")) for line in lines)
    for lower, upper in ranges:
        arr[lower : upper + 1] = np.zeros_like(arr[lower : upper + 1])
    print(np.sum(arr))
