from __future__ import annotations

from typing import ClassVar

with open("./2020/resources/7.txt") as f:
    lines = f.read().splitlines()


class Bag:
    lookup: ClassVar[dict[str, Bag]] = {}

    def __init__(self, colour: str) -> None:
        self.colour = colour
        self.contents: dict[Bag, int] = {}
        type(self).lookup[colour] = self

    @classmethod
    def get_by_name(cls, name: str) -> Bag:
        if name in cls.lookup:
            return cls.lookup[name]
        return cls(name)

    def can_contain(self, colour: str) -> bool:
        return any(b.colour == colour or b.can_contain(colour) for b in self.contents.keys())

    def num_inside(self) -> int:
        total = 0
        for b, num in self.contents.items():
            total += (1 + b.num_inside()) * num
        return total


def problem_1() -> None:
    for line in lines:
        bag_colour = " ".join(line.split(" contain ")[0].split()[:-1])
        bag = Bag.get_by_name(bag_colour)
        if "no other bags" not in line:
            contents = line.split("contain ")[1].strip(".").split(", ")
            for other_bag in contents:
                number_and_colour = other_bag.removesuffix("s").removesuffix(" bag")
                number = int(number_and_colour.split()[0])
                colour = " ".join(number_and_colour.split()[1:])
                bag.contents[Bag.get_by_name(colour)] = number

    can_contain_shiny_gold = 0
    for bag in Bag.lookup.values():
        if bag.can_contain("shiny gold"):
            can_contain_shiny_gold += 1
    print(can_contain_shiny_gold)


def problem_2() -> None:
    for line in lines:
        bag_colour = " ".join(line.split(" contain ")[0].split()[:-1])
        bag = Bag.get_by_name(bag_colour)
        if "no other bags" not in line:
            contents = line.split("contain ")[1].strip(".").split(", ")
            for other_bag in contents:
                number_and_colour = other_bag.removesuffix("s").removesuffix(" bag")
                number = int(number_and_colour.split()[0])
                colour = " ".join(number_and_colour.split()[1:])
                bag.contents[Bag.get_by_name(colour)] = number

    print(Bag.get_by_name("shiny gold").num_inside())
