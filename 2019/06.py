from __future__ import annotations

from functools import cache
from typing import ClassVar, Self

with open("./2019/resources/6.txt") as f:
    lines = f.read().splitlines()


class OrbitingBody:
    _lookup: ClassVar[dict[str, Self]] = {}

    def __init__(self, name: str) -> None:
        self.name = name
        type(self)._lookup[name] = self
        self.center_body: OrbitingBody

    @classmethod
    def get_by_name(cls, name: str) -> Self:
        if name in cls._lookup:
            return cls._lookup[name]
        return cls(name)

    @cache
    def direct_and_indirect_orbits(self) -> int:
        if self.name == "COM":
            return 0
        return 1 + self.center_body.direct_and_indirect_orbits()


def part_1() -> None:
    for line in lines:
        center, in_orbit = line.split(")")
        center_body = OrbitingBody.get_by_name(center)
        in_orbit_body = OrbitingBody.get_by_name(in_orbit)
        in_orbit_body.center_body = center_body

    print(sum(body.direct_and_indirect_orbits() for body in OrbitingBody._lookup.values()))


def part_2() -> None:
    for line in lines:
        center, in_orbit = line.split(")")
        center_body = OrbitingBody.get_by_name(center)
        in_orbit_body = OrbitingBody.get_by_name(in_orbit)
        in_orbit_body.center_body = center_body

    current = OrbitingBody.get_by_name("YOU").center_body
    cumulative_transfers = 0
    transfers_to: dict[str, int] = {}
    while current.name != "COM":
        current = current.center_body
        cumulative_transfers += 1
        transfers_to[current.name] = cumulative_transfers

    current = OrbitingBody.get_by_name("SAN").center_body
    cumulative_transfers = 0
    while current.name not in transfers_to:
        current = current.center_body
        cumulative_transfers += 1
    print(transfers_to[current.name] + cumulative_transfers)
