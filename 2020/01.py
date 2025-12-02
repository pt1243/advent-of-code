from itertools import combinations

with open("./2020/resources/1.txt") as f:
    nums = [int(x) for x in f.read().splitlines()]


def problem_1() -> None:
    for num_1, num_2 in combinations(nums, 2):
        if num_1 + num_2 == 2020:
            print(num_1 * num_2)
            return


def problem_2() -> None:
    for num_1, num_2, num_3 in combinations(nums, 3):
        if num_1 + num_2 + num_3 == 2020:
            print(num_1 * num_2 * num_3)
            return
