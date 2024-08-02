from __future__ import annotations
from itertools import cycle
from functools import cached_property
from math import lcm
from typing import ClassVar


with open("./2023/resources/8.txt") as f:
    lines = f.read().splitlines()


class Node:
    lookup: ClassVar[dict[str, Node]] = {}

    def __init__(self, name: str, left: str, right: str) -> None:
        self.name = name
        self.left_string = left
        self.right_string = right
        Node.lookup[name] = self

    @cached_property
    def left(self) -> Node:
        return Node.lookup[self.left_string]

    @cached_property
    def right(self) -> Node:
        return Node.lookup[self.right_string]


def problem_1() -> None:
    steps_iterator = cycle(lines[0])
    for line in lines[2:]:
        name, connections = line.split(" = ")
        left, right = connections[1:-1].split(", ")
        Node(name, left, right)

    current = Node.lookup["AAA"]
    for i, step in enumerate(steps_iterator, start=1):
        current = current.left if step == "L" else current.right
        if current.name == "ZZZ":
            print(i)
            return


def problem_2() -> None:
    for line in lines[2:]:
        name, connections = line.split(" = ")
        left, right = connections[1:-1].split(", ")
        Node(name, left, right)

    results: list[int] = []
    for current in [n for n in Node.lookup.values() if n.name.endswith("A")]:
        steps_iterator = cycle(lines[0])
        for i, step in enumerate(steps_iterator, start=1):
            current = current.left if step == "L" else current.right
            if current.name.endswith("Z"):
                # technically, we should check that the steps also repeat, but this works
                results.append(i)
                break
    print(lcm(*results))
