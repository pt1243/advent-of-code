from itertools import pairwise

from more_itertools import sliding_window

with open("./2021/resources/1.txt") as f:
    depths = [int(depth) for depth in f.read().splitlines()]


def problem_1() -> None:
    print(sum(1 for d1, d2 in pairwise(depths) if d2 > d1))


def problem_2() -> None:
    print(sum(1 for w1, w2 in pairwise(sliding_window(depths, 3)) if sum(w2) > sum(w1)))
