from __future__ import annotations

with open("./2018/resources/8.txt") as f:
    numbers = [int(n) for n in f.read().strip().split()]


class Node:
    def __init__(self, parent: Node | None = None) -> None:
        self.parent = parent
        self.children: list[Node] = []
        self.metadata_entries: list[int] = []

    def sum_metadata_entries_recursive(self) -> int:
        return sum(self.metadata_entries) + sum(child.sum_metadata_entries_recursive() for child in self.children)

    def get_value(self) -> int:
        if not self.children:
            return sum(self.metadata_entries)
        value = 0
        for idx in self.metadata_entries:
            if 0 <= idx - 1 < len(self.children):
                value += self.children[idx - 1].get_value()
        return value


def read_node_recursive(index: int, parent_node: Node | None = None) -> tuple[int, Node]:
    num_child_nodes, num_metadata_entries = numbers[index], numbers[index + 1]
    index += 2
    current_node = Node(parent_node)
    for _ in range(num_child_nodes):
        index, child_node = read_node_recursive(index, current_node)
        current_node.children.append(child_node)
    current_node.metadata_entries = numbers[index : index + num_metadata_entries]
    index += num_metadata_entries
    return index, current_node


def part_1() -> None:
    _, root = read_node_recursive(0)
    print(root.sum_metadata_entries_recursive())


def part_2() -> None:
    _, root = read_node_recursive(0)
    print(root.get_value())
