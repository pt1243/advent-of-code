from __future__ import annotations

import re
from collections import deque
from collections.abc import Callable
from dataclasses import dataclass
from math import lcm
from operator import add, mul

with open("./2022/resources/11.txt") as f:
    text = f.read().strip()


@dataclass
class Monkey:
    num: int
    items: deque[int]
    operation: Callable[[int, int], int]
    param: int | None
    divisor: int
    true_monkey: int
    false_monkey: int
    num_inspections: int = 0

    @classmethod
    def from_text(cls, text: str) -> list[Monkey]:
        monkeys: list[Monkey] = []
        int_pattern = re.compile(r"-?\d+")
        for block in text.split("\n\n"):
            lines = block.split("\n")
            num = next(map(int, re.findall(int_pattern, lines[0])))
            starting_items = deque(map(int, re.findall(int_pattern, lines[1])))
            operation = mul if "old * old" in lines[2] or "*" in lines[2] else add
            param = None if "old * old" in lines[2] else next(map(int, re.findall(int_pattern, lines[2])))
            divisor = next(map(int, re.findall(int_pattern, lines[3])))
            true_monkey = next(map(int, re.findall(int_pattern, lines[4])))
            false_monkey = next(map(int, re.findall(int_pattern, lines[5])))
            monkeys.append(Monkey(num, starting_items, operation, param, divisor, true_monkey, false_monkey))
        return monkeys


def throw_items(monkeys: list[Monkey], num_rounds: int, part_2: bool = False) -> int:
    lowest_common_multiple = lcm(*(monkey.divisor for monkey in monkeys))
    for _ in range(num_rounds):
        for monkey in monkeys:
            while monkey.items:
                item = monkey.items.popleft()
                monkey.num_inspections += 1
                if monkey.param is None:
                    item = monkey.operation(item, item)
                else:
                    item = monkey.operation(item, monkey.param)
                if part_2:
                    item %= lowest_common_multiple
                else:
                    item //= 3
                if item % monkey.divisor == 0:
                    monkeys[monkey.true_monkey].items.append(item)
                else:
                    monkeys[monkey.false_monkey].items.append(item)
    num_inspections = sorted((monkey.num_inspections for monkey in monkeys), reverse=True)
    return num_inspections[0] * num_inspections[1]


def part_1() -> None:
    monkeys = Monkey.from_text(text)
    print(throw_items(monkeys, 20))


def part_2() -> None:
    monkeys = Monkey.from_text(text)
    print(throw_items(monkeys, 10_000, part_2=True))
