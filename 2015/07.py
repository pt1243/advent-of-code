from __future__ import annotations

from typing import ClassVar, Protocol
from functools import cache


with open("./2015/resources/7.txt") as f:
    connections = f.read().splitlines()


class SupportsEvaluate(Protocol):
    def evaluate(self) -> int: ...


class Wire:
    lookup: ClassVar[dict[str, Wire]] = {}
    dep: SupportsEvaluate

    def __init__(self, input_string: str) -> None:
        self.name = input_string.split(" -> ")[1]
        Wire.lookup[self.name] = self

        if "AND" in input_string:
            self.dep = AND(input_string.split())
        elif "OR" in input_string:
            self.dep = OR(input_string.split())
        elif "NOT" in input_string:
            self.dep = NOT(input_string.split())
        elif "LSHIFT" in input_string:
            self.dep = LSHIFT(input_string.split())
        elif "RSHIFT" in input_string:
            self.dep = RSHIFT(input_string.split())
        else:
            self.dep = DIRECT(input_string.split()[0])

    @cache
    def evaluate(self) -> int:
        return self.dep.evaluate()


class DIRECT:
    def __init__(self, item: str) -> None:
        self.val: int | str = int(item) if item.isnumeric() else item

    def evaluate(self) -> int:
        return self.val if isinstance(self.val, int) else Wire.lookup[self.val].evaluate()


class AND:
    def __init__(self, split_line: list[str]) -> None:
        self.dep_1: DIRECT | str = DIRECT(split_line[0]) if split_line[0].isnumeric() else split_line[0]
        self.dep_2: DIRECT | str = DIRECT(split_line[2]) if split_line[2].isnumeric() else split_line[2]

    def evaluate(self) -> int:
        # this seems to be an issue with mypy
        val_1: SupportsEvaluate = Wire.lookup[self.dep_1] if isinstance(self.dep_1, str) else self.dep_1  # type: ignore[assignment]
        val_2: SupportsEvaluate = Wire.lookup[self.dep_2] if isinstance(self.dep_2, str) else self.dep_2  # type: ignore[assignment]
        return val_1.evaluate() & val_2.evaluate()


class OR:
    def __init__(self, split_line: list[str]) -> None:
        self.dep_1 = split_line[0]
        self.dep_2 = split_line[2]

    def evaluate(self) -> int:
        return Wire.lookup[self.dep_1].evaluate() | Wire.lookup[self.dep_2].evaluate()


class NOT:
    def __init__(self, split_line: list[str]) -> None:
        self.dep = split_line[1]

    def evaluate(self) -> int:
        return 65535 - Wire.lookup[self.dep].evaluate()


class LSHIFT:
    def __init__(self, split_line: list[str]) -> None:
        self.dep = split_line[0]
        self.shift = int(split_line[2])

    def evaluate(self) -> int:
        return Wire.lookup[self.dep].evaluate() << self.shift


class RSHIFT:
    def __init__(self, split_line: list[str]) -> None:
        self.dep = split_line[0]
        self.shift = int(split_line[2])

    def evaluate(self) -> int:
        return Wire.lookup[self.dep].evaluate() >> self.shift


def problem_1() -> None:
    for connection in connections:
        Wire(connection)

    print(Wire.lookup["a"].evaluate())


def problem_2() -> None:
    for connection in connections:
        Wire(connection)

    Wire(f"{Wire.lookup['a'].evaluate()} -> b")
    for wire in Wire.lookup.values():
        wire.evaluate.cache_clear()

    print(Wire.lookup["a"].evaluate())
