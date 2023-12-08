from __future__ import annotations
from typing import ClassVar


with open('./2017/resources/12.txt') as f:
    lines = [line.strip() for line in f]


class Program:
    lookup: ClassVar[dict[int, Program]] = {}
    used_groups: set[int] = {0}

    @classmethod
    def get_program(cls, id_num: int) -> Program:
        if id_num not in cls.lookup:
            cls.lookup[id_num] = Program(id_num)
        return cls.lookup[id_num]

    def __init__(self, id_num: int) -> None:
        self.id_num = id_num
        self.group = 0
        self.connections: list[Program] = []
    
    def extend_connections(self, connections: list[int]) -> None:
        for connection in connections:
            p = self.get_program(connection)
            if p not in self.connections:
                self.connections.append(p)


def problem_1() -> None:
    for line in lines:
        first, connections = line.split(" <-> ")
        p1 = Program.get_program(int(first))
        connections_list = [int(c) for c in connections.split(", ")]
        p1.extend_connections(connections_list)
        for connection in connections_list:
            p2 = Program.get_program(connection)
            p2.extend_connections([int(first)])

    p0 = Program.get_program(0)
    def search_recursive(p: Program):
        p.group = 1
        for c in p.connections:
            if not c.group:
                search_recursive(c)
    search_recursive(p0)
    
    print(len([p for p in Program.lookup.values() if p.group]))


def problem_2() -> None:
    for line in lines:
        first, connections = line.split(" <-> ")
        p1 = Program.get_program(int(first))
        connections_list = [int(c) for c in connections.split(", ")]
        p1.extend_connections(connections_list)
        for connection in connections_list:
            p2 = Program.get_program(connection)
            p2.extend_connections([int(first)])

    def search_recursive_groups(p: Program, group_num: int) -> None:
        p.group = group_num
        Program.used_groups.add(group_num)
        for c in p.connections:
            if not c.group:
                search_recursive_groups(c, group_num)

    for p in Program.lookup.values():
        if not p.group:
            search_recursive_groups(p, max(Program.used_groups) + 1)

    print(max(Program.used_groups))
