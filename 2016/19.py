from math import floor, log2


num_elves = 3018458


def problem_1() -> None:
    # https://www.youtube.com/watch?v=uCsD3ZGzMgE
    max_pow_2 = floor(log2(num_elves))
    difference = num_elves - 2 ** max_pow_2
    print(2 * difference + 1)


def problem_2() -> None:
    pass
