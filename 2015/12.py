from __future__ import annotations

import json
from collections.abc import Iterable, Mapping
from typing import Union

with open("./2015/resources/12.txt") as f:
    data = json.load(f)

IterableToSum = list[Union[int, str, "IterableToSum"]] | Mapping[str | int, Union[int, str, "IterableToSum"]]


def sum_recursive(iterable: IterableToSum, ignore_red: bool = False) -> int:
    total = 0
    red_found = False
    if isinstance(iterable, Mapping):
        for key, value in iterable.items():
            if key == "red" or value == "red":
                red_found = True
                if ignore_red:
                    break
            if isinstance(key, int):
                total += key
            if isinstance(value, int):
                total += value
            if isinstance(value, Iterable) and not isinstance(value, str):
                total += sum_recursive(value, ignore_red=ignore_red)
        if ignore_red and red_found:
            return 0
    else:
        for element in iterable:
            if isinstance(element, Iterable) and not isinstance(element, str):
                total += sum_recursive(element, ignore_red=ignore_red)
            elif isinstance(element, int):
                total += element
    return total


def part_1() -> None:
    print(sum_recursive(data))


def part_2() -> None:
    print(sum_recursive(data, ignore_red=True))
