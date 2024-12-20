from __future__ import annotations
from collections.abc import Iterator
from operator import methodcaller
from typing import NamedTuple
from more_itertools import split_before


with open("./2022/resources/7.txt") as f:
    lines = f.read().splitlines()


class Directory:
    def __init__(self, name: str):
        self.name = name
        self.items: list[File | Directory] = []
        self.parent: Directory

    def size(self) -> int:
        return sum(item.size if isinstance(item, File) else item.size() for item in self.items)

    def iterate(self) -> Iterator[Directory]:
        yield self
        for item in self.items:
            if isinstance(item, Directory):
                yield from item.iterate()


class File(NamedTuple):
    name: str
    size: int


def problem_1() -> None:
    root = Directory("/")
    root.parent = root
    current_directory = root
    for command, *outputs in split_before(lines, lambda line: line.startswith("$")):
        if command.startswith("$ cd"):
            if command == "$ cd /":
                current_directory = root
            elif command == "$ cd ..":
                current_directory = current_directory.parent
            else:
                current_directory = next(
                    d for d in current_directory.items if isinstance(d, Directory) and d.name == command.split()[-1]
                )
            continue
        for output in outputs:
            if output.startswith("dir"):
                subdirectory = Directory(output.split()[1])
                subdirectory.parent = current_directory
                current_directory.items.append(subdirectory)
            else:
                current_directory.items.append(File(output.split()[1], int(output.split()[0])))

    total = 0
    for d in root.iterate():
        size = d.size()
        if size <= 100000:
            total += size
    print(total)


def problem_2() -> None:
    root = Directory("/")
    root.parent = root
    current_directory = root
    for command, *outputs in split_before(lines, lambda line: line.startswith("$")):
        if command.startswith("$ cd"):
            if command == "$ cd /":
                current_directory = root
            elif command == "$ cd ..":
                current_directory = current_directory.parent
            else:
                current_directory = next(
                    d for d in current_directory.items if isinstance(d, Directory) and d.name == command.split()[-1]
                )
            continue
        for output in outputs:
            if output.startswith("dir"):
                subdirectory = Directory(output.split()[1])
                subdirectory.parent = current_directory
                current_directory.items.append(subdirectory)
            else:
                current_directory.items.append(File(output.split()[1], int(output.split()[0])))

    required_space = 30000000 - (70000000 - root.size())
    smallest = min((d for d in root.iterate() if d.size() >= required_space), key=methodcaller("size"))
    print(smallest.size())
