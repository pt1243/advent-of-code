from typing import Sequence
from functools import reduce
from operator import mul
from itertools import combinations
from math import floor

import numpy as np


with open('./2015/resources/24.txt') as f:
    weights = {int(line.strip()) for line in f}

def can_partition_into_two(S: Sequence[int]) -> bool:
    n = len(S)
    K = sum(S)
    P = np.empty((floor(K / 2) + 1, n + 1), dtype=bool)

    P[:, 0] = np.zeros(floor(K / 2) + 1)
    P[0, :] = np.ones(n + 1)

    for i in range(1, floor(K / 2) + 1):
        for j in range(1, n + 1):
            x = S[j - 1]
            if i - x >= 0:
                P[i, j] = P[i, j - 1] or P[i - x, j - 1]
            else:
                P[i, j] = P[i, j - 1]

    return P[floor(K / 2), n]


def can_partition_into_three(nums: set[int], target: int) -> bool:
    # essentially just the solution to problem 1
    num_second_group = 1
    while True:
        for second_group_choice in combinations(nums, num_second_group):
            if sum(second_group_choice) == target:
                # now check that the remainder can be partitioned into 2
                if can_partition_into_two(tuple(nums - set(second_group_choice))):
                    return True
        num_second_group += 1
        if num_second_group >= len(nums):
            return False


def problem_1() -> None:
    target = sum(weights) // 3

    min_qe = float('inf')
    num_first_group = 1
    found = False

    while True:
        for present_choices in combinations(weights, num_first_group):
            if sum(present_choices) == target:  # check that the remaining present choices can be split
                if can_partition_into_two(tuple(weights - set(present_choices))):
                    qe = reduce(mul, present_choices)
                    if qe < min_qe:
                        min_qe = qe
                    found = True
        if found:
            print(min_qe)
            break
        num_first_group += 1


def problem_2() -> None:
    target = sum(weights) // 4

    min_qe = float('inf')
    num_first_group = 1
    found = False

    while True:
        for first_group_choice in combinations(weights, num_first_group):
            if sum(first_group_choice) == target:
                if can_partition_into_three(weights - set(first_group_choice), target):
                    qe = reduce(mul, first_group_choice)
                    if qe < min_qe:
                        min_qe = qe
                    found = True
        if found:
            print(min_qe)
            break
        num_first_group += 1
