from collections.abc import Sequence
from math import floor, log10

with open("./2024/resources/7.txt") as f:
    lines = f.read().splitlines()


def can_reach(nums: Sequence[int], target: int, use_conat: bool = False) -> bool:
    if len(nums) == 1:
        return target == nums[0]
    last = nums[-1]
    quotient, remainder = divmod(target, last)
    if remainder == 0 and can_reach(nums[:-1], quotient, use_conat):
        return True
    if last <= target and can_reach(nums[:-1], target - last, use_conat):
        return True
    if use_conat:
        digits_in_last = 1 + floor(log10(last))
        if target % (10**digits_in_last) == last:
            return can_reach(nums[:-1], target // (10**digits_in_last), use_conat)
    return False


def problem_1() -> None:
    total = 0
    for line in lines:
        left, right = line.split(": ")
        target = int(left)
        nums = [int(x) for x in right.split()]
        if can_reach(nums, target):
            total += target
    print(total)


def problem_2() -> None:
    total = 0
    for line in lines:
        left, right = line.split(": ")
        target = int(left)
        nums = [int(x) for x in right.split()]
        if can_reach(nums, target, use_conat=True):
            total += target
    print(total)
