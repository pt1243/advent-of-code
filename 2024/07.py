from functools import reduce
from itertools import product
from operator import add, mul


with open("./2024/resources/7.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    total = 0
    for line in lines:
        left, right = line.split(": ")
        target = int(left)
        nums = [int(x) for x in right.split()]
        for operations in product((add, mul), repeat=len(nums) - 1):
            ops = iter(operations)
            if reduce(lambda x, y: next(ops)(x, y), nums) == target:
                total += target
                break
    print(total)


def problem_2() -> None:
    total = 0
    for line in lines:
        left, right = line.split(": ")
        target = int(left)
        nums = [int(x) for x in right.split()]
        for operations in product((add, mul, lambda x, y: int(str(x) + str(y))), repeat=len(nums) - 1):
            ops = iter(operations)
            if reduce(lambda x, y: next(ops)(x, y), nums) == target:
                total += target
                break
    print(total)
