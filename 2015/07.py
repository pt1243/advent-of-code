from __future__ import annotations
from typing import ClassVar, Callable
from functools import cache


with open("./2015/resources/7.txt") as f:
    connections = f.read().splitlines()


class Wire:
    lookup: ClassVar[dict[str, Wire]] = {}

    def __init__(self, input_string: str) -> None:
        split = input_string.split(" -> ")
        self._left = split[0]
        self.name = split[1]
        type(self).lookup[self.name] = self
        self.evaluate: Callable[[], int]

        if "AND" in input_string:
            self.evaluate = lambda: self.resolve(self._left.split()[0]) & self.resolve(self._left.split()[2])
        elif "OR" in input_string:
            self.evaluate = lambda: self.resolve(self._left.split()[0]) | self.resolve(self._left.split()[2])
        elif "LSHIFT" in input_string:
            self.evaluate = lambda: self.resolve(self._left.split()[0]) << self.resolve(self._left.split()[2])
        elif "RSHIFT" in input_string:
            self.evaluate = lambda: self.resolve(self._left.split()[0]) >> self.resolve(self._left.split()[2])
        elif "NOT" in input_string:
            self.evaluate = lambda: 65535 - self.resolve(self._left.split()[1])
        else:
            self.evaluate = lambda: self.resolve(self._left)

    @classmethod
    @cache
    def resolve(cls, arg: str) -> int:
        if arg.isnumeric():
            return int(arg)
        return cls.lookup[arg].evaluate()


def problem_1() -> None:
    for connection in connections:
        Wire(connection)

    print(Wire.lookup["a"].evaluate())


def problem_2() -> None:
    for connection in connections:
        Wire(connection)

    Wire(f"{Wire.lookup['a'].evaluate()} -> b")
    for wire in Wire.lookup.values():
        wire.resolve.cache_clear()

    print(Wire.lookup["a"].evaluate())
