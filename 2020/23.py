from __future__ import annotations
from itertools import pairwise
from typing import Generic, TypeVar


with open("./2020/resources/23.txt") as f:
    cups = [int(char) for char in f.read().strip()]


T = TypeVar("T")


class Node(Generic[T]):
    def __init__(self, value: T) -> None:
        self.value = value
        self.left: Node[T]
        self.right: Node[T]


def play_cups(cups: list[int], num_moves: int, part_2: bool = False) -> dict[int, Node[int]]:
    nodes = {cup: Node(cup) for cup in cups}
    if part_2:
        for i in range(10, 1_000_001):
            nodes[i] = Node(i)
    for node_1, node_2 in pairwise(nodes.values()):
        node_1.right = node_2
        node_2.left = node_1
    if part_2:
        nodes[cups[0]].left = nodes[1_000_000]
        nodes[1_000_000].right = nodes[cups[0]]
    else:
        nodes[cups[0]].left = nodes[cups[-1]]
        nodes[cups[-1]].right = nodes[cups[0]]

    current_cup = nodes[cups[0]]
    size = 9 if not part_2 else 1_000_000
    for _ in range(num_moves):
        first = current_cup.right
        second = first.right
        third = second.right
        fourth = third.right

        current_cup.right = fourth
        fourth.left = current_cup

        picked_up_values = {first.value, second.value, third.value}
        destination_value = current_cup.value - 1
        if destination_value == 0:
            destination_value = size
        while destination_value in picked_up_values:
            destination_value -= 1
            if destination_value == 0:
                destination_value = size
        destination = nodes[destination_value]
        right = destination.right
        destination.right = first
        first.left = destination
        third.right = right
        right.left = third

        current_cup = current_cup.right
    return nodes


def problem_1() -> None:
    nodes = play_cups(cups, 100)
    current = nodes[1]
    result = ""
    for _ in range(8):
        current = current.right
        result += str(current.value)
    print(result)


def problem_2() -> None:
    nodes = play_cups(cups, 10_000_000, part_2=True)
    one = nodes[1]
    print(one.right.value * one.right.right.value)
