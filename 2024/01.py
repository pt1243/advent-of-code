from collections import Counter

with open("./2024/resources/1.txt") as f:
    nums = [int(x) for x in f.read().strip().split()]


def problem_1() -> None:
    print(sum(abs(id_1 - id_2) for id_1, id_2 in zip(sorted(nums[::2]), sorted(nums[1::2]))))


def problem_2() -> None:
    col_1 = Counter(nums[::2])
    col_2 = Counter(nums[1::2])
    print(sum(id_1 * times * col_2[id_1] for id_1, times in col_1.items()))
