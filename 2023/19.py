from __future__ import annotations

from math import prod
from typing import ClassVar

with open("./2023/resources/19.txt") as f:
    input_text = f.read().strip()


class Workflow:
    part_attributes = ("x", "m", "a", "s")
    lookup: ClassVar[dict[str, Workflow]] = {}

    def __init__(self, name: str, rules: list[str]) -> None:
        self.name = name
        type(self).lookup[name] = self

        condition, destination = rules[0].split(":")
        self.index = self.part_attributes.index(condition[0])
        self.decision_value = int(condition[2:])

        if condition[1] == ">":
            self.decision_value += 1  # left if <, right if >= decision value

        if destination == "A":
            self.left: bool | str = True
        elif destination == "R":
            self.left = False
        else:
            self.left = destination

        if len(rules) == 2:
            right_destination = rules[1]
            if right_destination == "A":
                self.right: bool | str = True
            elif right_destination == "R":
                self.right = False
            else:
                self.right = right_destination
        else:
            if "_" in name:
                next_num = int(name[name.index("_") + 1 :]) + 1
            else:
                next_num = 1
            new_name = f"{name}_{next_num}"
            self.right = new_name
            type(self)(new_name, rules[1:])
        if condition[1] == ">":
            self.left, self.right = self.right, self.left

    def evaluate_single(self, item: tuple[int, ...]) -> bool:
        target = self.left if item[self.index] < self.decision_value else self.right
        if isinstance(target, bool):
            return target
        return type(self).lookup[target].evaluate_single(item)

    def num_accepted(self, input_range: list[tuple[int, int]]) -> int:
        if not input_range:
            return 0
        low, high = input_range[self.index]
        if self.decision_value < low:
            left_range = []
            right_range = input_range
        elif self.decision_value > high:
            left_range = input_range
            right_range = []
        else:
            left_range_values = (low, self.decision_value - 1)
            right_range_values = (self.decision_value, high)
            left_range = input_range.copy()
            left_range[self.index] = left_range_values
            right_range = input_range.copy()
            right_range[self.index] = right_range_values
        total = 0
        if self.left is True:
            total += prod(item[1] - item[0] + 1 for item in left_range)
        elif isinstance(self.left, str):
            total += type(self).lookup[self.left].num_accepted(left_range)
        if self.right is True:
            total += prod(item[1] - item[0] + 1 for item in right_range)
        elif isinstance(self.right, str):
            total += type(self).lookup[self.right].num_accepted(right_range)
        return total


def part_1() -> None:
    workflows, parts = input_text.split("\n\n")
    for workflow in workflows.split("\n"):
        paren_index = workflow.index("{")
        name = workflow[:paren_index]
        rules = workflow[paren_index + 1 : -1].split(",")
        Workflow(name, rules)

    sum_of_rating_numbers = 0
    for part_text in parts.split("\n"):
        items = part_text[1:-1].split(",")
        part = tuple(int(item[2:]) for item in items)
        if Workflow.lookup["in"].evaluate_single(part):
            sum_of_rating_numbers += sum(part)
    print(sum_of_rating_numbers)


def part_2() -> None:
    workflows = input_text.split("\n\n")[0]
    for workflow in workflows.split("\n"):
        paren_index = workflow.index("{")
        name = workflow[:paren_index]
        rules = workflow[paren_index + 1 : -1].split(",")
        Workflow(name, rules)

    print(Workflow.lookup["in"].num_accepted([(1, 4000)] * 4))
