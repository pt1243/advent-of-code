from __future__ import annotations
from collections import Counter, deque
from itertools import pairwise
import random
from typing import ClassVar


random.seed("AOC2023")


with open("./2023/resources/25.txt") as f:
    lines = [line.strip() for line in f]


class Component:
    lookup: ClassVar[dict[str, Component]] = {}

    def __init__(self, name: str, connections: list[str]) -> None:
        self.name = name
        type(self).lookup[name] = self
        self._connection_names = connections
        self.connections: set[Component] = set()
        self.reachable: bool = False

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.name!r}, {self._connection_names!r})"

    @classmethod
    def update_connections(cls) -> None:
        for c in cls.lookup.values():
            for connection_name in c._connection_names:
                c.connections.add(cls.lookup[connection_name])


def problem_1() -> None:
    all_connections: list[tuple[str, str]] = []
    for line in lines:
        left, right = line.split(": ")
        names = right.split()
        if left in Component.lookup:
            Component.lookup[left]._connection_names.extend(names)
        else:
            Component(left, names)
        for name in names:
            all_connections.append((left, name))
            if name in Component.lookup:
                Component.lookup[name]._connection_names.append(left)
            else:
                Component(name, [left])
    Component.update_connections()
    components = list(Component.lookup.values())

    def path_between(start: Component, end: Component) -> list[tuple[str, str]]:
        queue: deque[tuple[Component, list[Component]]] = deque([(start, [])])
        visited = set()
        while queue:
            current, path = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            new_path = path + [current]
            if current == end:
                edges = []
                for c1, c2 in pairwise(new_path):
                    first_name = c1.name
                    second_name = c2.name
                    edges.append((first_name, second_name) if first_name < second_name else (second_name, first_name))
                return edges
            for neighbour in current.connections:
                if neighbour not in visited:
                    queue.append((neighbour, new_path))

    frequencies: Counter[tuple[str, str]] = Counter()
    num_points_to_check = 5000
    for start, end in zip(
        random.choices(components, k=num_points_to_check), random.choices(components, k=num_points_to_check)
    ):
        edges = path_between(start, end)
        frequencies.update(edges)
    (c1_str, c2_str), (c3_str, c4_str), (c5_str, c6_str) = (item[0] for item in frequencies.most_common(3))
    c1, c2 = Component.lookup[c1_str], Component.lookup[c2_str]
    c3, c4 = Component.lookup[c3_str], Component.lookup[c4_str]
    c5, c6 = Component.lookup[c5_str], Component.lookup[c6_str]
    c1.connections.remove(c2)
    c2.connections.remove(c1)
    c3.connections.remove(c4)
    c4.connections.remove(c3)
    c5.connections.remove(c6)
    c6.connections.remove(c5)

    def mark_recursive(c: Component):
        c.reachable = True
        for neighbour in c.connections:
            if not neighbour.reachable:
                mark_recursive(neighbour)

    mark_recursive(components[0])
    first_group = sum(1 for c in components if c.reachable)
    second_group = len(components) - first_group
    print(first_group * second_group)
