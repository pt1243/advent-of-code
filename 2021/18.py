from __future__ import annotations

from ast import literal_eval
from copy import deepcopy
from dataclasses import dataclass
from functools import reduce
from math import ceil, floor
from typing import Union

with open("./2021/resources/18.txt") as f:
    lines = f.read().splitlines()


SnailfishList = list[Union[int, "SnailfishList"]]


@dataclass
class SnailfishNumber:
    left: SnailfishNumber | RegularNumber
    right: SnailfishNumber | RegularNumber
    parent: SnailfishNumber | None = None


@dataclass
class RegularNumber:
    value: int
    parent: SnailfishNumber | None = None


def parse_snailfish_num(num: SnailfishList) -> SnailfishNumber:
    left = RegularNumber(num[0]) if isinstance(num[0], int) else parse_snailfish_num(num[0])
    right = RegularNumber(num[1]) if isinstance(num[1], int) else parse_snailfish_num(num[1])
    result = SnailfishNumber(left, right)
    left.parent = result
    right.parent = result
    return result


def reduce_snailfish_num(num: SnailfishNumber) -> SnailfishNumber:
    def find_pair_to_explode(num: SnailfishNumber, depth: int = 0) -> SnailfishNumber | None:
        if depth == 4:
            return num
        if isinstance(num.left, SnailfishNumber):
            value = find_pair_to_explode(num.left, depth + 1)
            if value is not None:
                return value
        if isinstance(num.right, SnailfishNumber):
            value = find_pair_to_explode(num.right, depth + 1)
            if value is not None:
                return value
        return None

    def traverse_pre(
        num: SnailfishNumber | RegularNumber, results: list[SnailfishNumber | RegularNumber] | None = None
    ) -> list[SnailfishNumber | RegularNumber]:
        if results is None:
            results = []
        results.append(num)
        if isinstance(num, SnailfishNumber):
            traverse_pre(num.left, results)
            traverse_pre(num.right, results)
        return results

    def traverse_post(
        num: SnailfishNumber | RegularNumber, results: list[SnailfishNumber | RegularNumber] | None = None
    ) -> list[SnailfishNumber | RegularNumber]:
        if results is None:
            results = []
        if isinstance(num, SnailfishNumber):
            traverse_post(num.left, results)
            traverse_post(num.right, results)
        results.append(num)
        return results

    while True:
        pair_to_explode = find_pair_to_explode(num)
        if pair_to_explode is not None:
            if not isinstance(pair_to_explode.left, RegularNumber) or not isinstance(
                pair_to_explode.right, RegularNumber
            ):
                raise ValueError("exploding pair must consist of two regular numbers")
            if pair_to_explode.parent is None:
                raise ValueError("exploding pair must have a parent")

            flattened_number_left = traverse_pre(num)
            target_index_left = [i for i, val in enumerate(flattened_number_left) if val is pair_to_explode][0]
            left_regular_numbers = [
                val
                for i, val in enumerate(flattened_number_left)
                if isinstance(val, RegularNumber) and i < target_index_left
            ]
            if left_regular_numbers:
                left_regular_numbers[-1].value += pair_to_explode.left.value

            flattened_number_right = traverse_post(num)
            target_index_right = [i for i, val in enumerate(flattened_number_right) if val is pair_to_explode][0]
            right_regular_numbers = [
                val
                for i, val in enumerate(flattened_number_right)
                if isinstance(val, RegularNumber) and i > target_index_right
            ]
            if right_regular_numbers:
                right_regular_numbers[0].value += pair_to_explode.right.value

            parent = pair_to_explode.parent
            use_left = parent.left is pair_to_explode
            if use_left:
                parent.left = RegularNumber(0, parent)
            else:
                parent.right = RegularNumber(0, parent)
            continue

        large_regular_numbers = [val for val in traverse_pre(num) if isinstance(val, RegularNumber) and val.value >= 10]
        if not large_regular_numbers:
            break

        number_to_split = large_regular_numbers[0]
        if number_to_split.parent is None:
            raise ValueError("splitting top level num")
        parent = number_to_split.parent
        replacement = SnailfishNumber(
            RegularNumber(floor(number_to_split.value / 2)), RegularNumber(ceil(number_to_split.value / 2))
        )
        replacement.parent = parent
        replacement.left.parent = replacement
        replacement.right.parent = replacement

        use_left = parent.left is number_to_split
        if use_left:
            parent.left = replacement
        else:
            parent.right = replacement

    return num


def add_snailfish_numbers(num_1: SnailfishNumber, num_2: SnailfishNumber) -> SnailfishNumber:
    result = SnailfishNumber(num_1, num_2)
    num_1.parent = result
    num_2.parent = result
    return reduce_snailfish_num(result)


def magnitude(num: SnailfishNumber | RegularNumber) -> int:
    if isinstance(num, RegularNumber):
        return num.value
    return 3 * magnitude(num.left) + 2 * magnitude(num.right)


def part_1() -> None:
    numbers = [parse_snailfish_num(literal_eval(line)) for line in lines]
    final_sum = reduce(add_snailfish_numbers, numbers)
    print(magnitude(final_sum))


def part_2() -> None:
    numbers = [parse_snailfish_num(literal_eval(line)) for line in lines]
    max_magnitude = 0
    for num_1 in numbers:
        for num_2 in numbers:
            if num_1 is num_2:
                continue
            max_magnitude = max(max_magnitude, magnitude(add_snailfish_numbers(deepcopy(num_1), deepcopy(num_2))))
    print(max_magnitude)
