from __future__ import annotations

from collections.abc import Callable
from operator import add, floordiv, mul, sub
from typing import ClassVar, cast

with open("./2022/resources/21.txt") as f:
    lines = f.read().splitlines()


class Monkey:
    lookup: ClassVar[dict[str, Monkey]] = {}

    def __init__(self, line: str):
        name, right = line.split(": ")
        split = right.split()
        self.name = name
        type(self).lookup[name] = self
        self.evaluate: Callable[[], int]
        self.parent: Monkey
        if right.isnumeric():
            self.left = None
            self.right = None
            self.op = None
            self.evaluate = lambda: int(right)
        else:
            self.left = split[0]
            self.op = split[1]
            self.right = split[2]
            self.evaluate = lambda: {"+": add, "-": sub, "*": mul, "/": floordiv}[cast(str, self.op)](
                self.resolve(cast(str, self.left)), self.resolve(cast(str, self.right))
            )

    @classmethod
    def resolve(cls, name: str) -> int:
        return cls.lookup[name].evaluate()

    def set_parent(self) -> None:
        if self.op is not None:
            type(self).lookup[cast(str, self.left)].parent = self
            type(self).lookup[cast(str, self.right)].parent = self


def problem_1() -> None:
    for line in lines:
        Monkey(line)
    print(Monkey.lookup["root"].evaluate())


def problem_2() -> None:
    for line in lines:
        Monkey(line)
    for monkey in Monkey.lookup.values():
        monkey.set_parent()

    parents: list[Monkey] = []
    current = Monkey.lookup["humn"]
    while current.name != "root":
        parents.append(current)
        current = current.parent
    last = parents.pop().name

    root = Monkey.lookup["root"]
    target_value = Monkey.resolve(cast(str, root.left if root.right == last else root.right))
    while parents:
        current = parents.pop()
        parent = current.parent
        current_is_left = parent.left == current.name
        other_value = Monkey.resolve(cast(str, parent.right if current_is_left else parent.left))
        if parent.op == "+":
            target_value -= other_value
        elif parent.op == "*":
            target_value //= other_value
        elif parent.op == "-":
            if current_is_left:
                target_value += other_value
            else:
                target_value = other_value - target_value
        else:
            if current_is_left:
                target_value *= other_value
            else:
                target_value //= other_value
    print(target_value)
