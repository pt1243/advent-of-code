import ast
from functools import cmp_to_key
from itertools import zip_longest
from typing import Union, cast

with open("./2022/resources/13.txt") as f:
    text = f.read().strip()


RecursiveList = list[Union[int, "RecursiveList"]]


def compare_values(first: int | RecursiveList, second: int | RecursiveList) -> bool | None:
    if isinstance(first, int) and isinstance(second, int):
        return None if first == second else first < second
    if isinstance(first, list) and isinstance(second, list):
        for item_1, item_2 in zip_longest(first, second, fillvalue=None):
            if item_1 is None:
                return True
            if item_2 is None:
                return False
            result = compare_values(item_1, item_2)
            if result is not None:
                return result
        return None
    # mixed values
    if isinstance(first, int):
        return compare_values([first], second)
    return compare_values(first, [second])


def problem_1() -> None:
    total = 0
    for i, comparison in enumerate(text.split("\n\n"), start=1):
        first, second = comparison.split("\n")
        result = compare_values(ast.literal_eval(first), ast.literal_eval(second))
        if result is None:
            raise ValueError("top-level comparison should not return None")
        total += i * result
    print(total)


def problem_2() -> None:
    first_divider = RecursiveList([[2]])
    second_divider = RecursiveList([[6]])
    all_packets: list[RecursiveList] = [first_divider, second_divider]
    for line in text.split("\n"):
        if line:
            all_packets.append(ast.literal_eval(line))

    comparison_func = cmp_to_key(
        lambda a, b: -1 if compare_values(cast(RecursiveList, a), cast(RecursiveList, b)) else 1
    )
    sorted_packets = sorted(all_packets, key=comparison_func)

    print((sorted_packets.index(first_divider) + 1) * (sorted_packets.index(second_divider) + 1))
