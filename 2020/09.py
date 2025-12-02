from itertools import combinations

with open("./2020/resources/9.txt") as f:
    nums = [int(x) for x in f.read().splitlines()]


def problem_1() -> None:
    preamble_length = 25
    for i, num in enumerate(nums[preamble_length:], start=preamble_length):
        previous = nums[i - preamble_length : i]
        if not any(x1 + x2 == num for x1, x2 in combinations(previous, 2)):
            print(num)
            return


def problem_2() -> None:
    preamble_length = 25
    for i, num in enumerate(nums[preamble_length:], start=preamble_length):
        previous = nums[i - preamble_length : i]
        if not any(x1 + x2 == num for x1, x2 in combinations(previous, 2)):
            invalid_num = num
            break

    for i in range(len(nums)):
        for j in range(i, len(nums)):
            total = sum(nums[i : j + 1])
            if total == invalid_num:
                print(min(nums[i : j + 1]) + max(nums[i : j + 1]))
                return
            if total > invalid_num:
                break
