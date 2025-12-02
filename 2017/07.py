from __future__ import annotations

from typing import ClassVar

with open("./2017/resources/7.txt") as f:
    lines = f.read().splitlines()


class Program:
    lookup: ClassVar[dict[str, Program]] = {}

    def __init__(self, name: str, weight: int, children: list[str]) -> None:
        self.name = name
        self.weight = weight
        self.children = children
        Program.lookup[name] = self

    def get_weight(self) -> int:
        return self.weight + sum(Program.lookup[p].get_weight() for p in self.children)

    def is_balanced(self) -> bool:
        if not self.children:
            return True
        target = Program.lookup[self.children[0]].get_weight()
        return all(Program.lookup[child].get_weight() == target for child in self.children)


def problem_1() -> None:
    for line in lines:
        split = line.split(" -> ")
        name = split[0].split()[0]
        weight = int(split[0].split()[1][1:-1])
        children = [p for p in split[1].split(", ")] if " -> " in line else []
        Program(name, weight, children)
    current = next(iter(Program.lookup))
    while True:
        for program in Program.lookup.values():
            if current in program.children:
                current = program.name
                break
        else:
            print(current)
            return


def problem_2() -> None:
    for line in lines:
        split = line.split(" -> ")
        name = split[0].split()[0]
        weight = int(split[0].split()[1][1:-1])
        children = [p for p in split[1].split(", ")] if " -> " in line else []
        Program(name, weight, children)

    for p in Program.lookup.values():
        if not p.is_balanced():
            unbalanced = p
            break

    def search_children(p: Program) -> Program:
        for child_name in p.children:
            child = Program.lookup[child_name]
            if not child.is_balanced():
                return search_children(child)
        return p

    deepest_unbalanced = search_children(unbalanced)
    weights = [Program.lookup[child_name].get_weight() for child_name in deepest_unbalanced.children]
    for child_name in deepest_unbalanced.children:
        child = Program.lookup[child_name]
        if weights.count(child.get_weight()) == 1:
            print(
                [w for w in weights if w != child.weight][0]
                - sum(Program.lookup[c].get_weight() for c in child.children)
            )
            return
