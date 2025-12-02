from __future__ import annotations

import re
from collections.abc import Iterator
from itertools import product
from typing import NamedTuple, Self

with open("./2021/resources/22.txt") as f:
    lines = f.read().splitlines()


class Box(NamedTuple):
    min_x: int
    max_x: int
    min_y: int
    max_y: int
    min_z: int
    max_z: int

    @classmethod
    def from_inclusive_ranges(cls, min_x: int, max_x: int, min_y: int, max_y: int, min_z: int, max_z: int) -> Self:
        return cls(min_x, max_x + 1, min_y, max_y + 1, min_z, max_z + 1)

    def intersects_with(self, other: Box) -> bool:
        return (
            not (self.max_x <= other.min_x or self.min_x >= other.max_x)
            and not (self.max_y <= other.min_y or self.min_y >= other.max_y)
            and not (self.max_z <= other.min_z or self.min_z >= other.max_z)
        )

    def is_within(self, other: Box) -> bool:
        return (
            (self.min_x >= other.min_x and self.max_x <= other.max_x)
            and (self.min_y >= other.min_y and self.max_y <= other.max_y)
            and (self.min_z >= other.min_z and self.max_z <= other.max_z)
        )

    def volume(self) -> int:
        return (self.max_x - self.min_x) * (self.max_y - self.min_y) * (self.max_z - self.min_z)

    def divide_into_subboxes(self, other: Box) -> Iterator[Box]:
        x1, x2, x3, x4 = sorted((self.min_x, self.max_x - 1, other.min_x, other.max_x - 1))
        y1, y2, y3, y4 = sorted((self.min_y, self.max_y - 1, other.min_y, other.max_y - 1))
        z1, z2, z3, z4 = sorted((self.min_z, self.max_z - 1, other.min_z, other.max_z - 1))
        for x_bound, y_bound, z_bound in product(
            [(x1, x2 - 1), (x2, x3), (x3 + 1, x4)],
            [(y1, y2 - 1), (y2, y3), (y3 + 1, y4)],
            [(z1, z2 - 1), (z2, z3), (z3 + 1, z4)],
        ):
            if x_bound[1] >= x_bound[0] and y_bound[1] >= y_bound[0] and z_bound[1] >= z_bound[0]:
                subbox = Box.from_inclusive_ranges(*x_bound, *y_bound, *z_bound)
                if subbox.is_within(self):
                    yield subbox


def run_cubes(part_2: bool = False) -> int:
    ints = re.compile(r"-?\d+")
    current_on_cubes: list[Box] = []
    for line in lines:
        current_line_box = Box.from_inclusive_ranges(*map(int, re.findall(ints, line)))
        if not part_2 and (
            current_line_box.min_x < -50
            or current_line_box.max_x > 51
            or current_line_box.min_y < -50
            or current_line_box.max_y > 51
            or current_line_box.min_z < -50
            or current_line_box.max_z > 51
        ):
            continue
        if line.startswith("on"):
            # if we are turning on cubes, we want to find the intersection with all current on cubes, and discard those
            # which are already on, before we add these to the on set
            boxes_to_process = [current_line_box]  # boxes we want to add, but which we need to check for intersection
            while boxes_to_process:
                current_box = boxes_to_process.pop()
                for existing_on_box in current_on_cubes:
                    if current_box.intersects_with(existing_on_box):
                        if not current_box.is_within(existing_on_box):
                            boxes_to_process.extend(current_box.divide_into_subboxes(existing_on_box))
                        break
                else:
                    # no intersections found - add to currently on cubes
                    current_on_cubes.append(current_box)
        else:
            # if we are turning off cubes, we want to iterate through the on cubes
            # if a region of cubes that are on is fully within the cube to turn off, remove it
            cubes_to_keep_on: list[Box] = []
            while current_on_cubes:
                current_box = current_on_cubes.pop()
                if current_box.intersects_with(current_line_box):
                    if not current_box.is_within(current_line_box):
                        current_on_cubes.extend(current_box.divide_into_subboxes(current_line_box))
                else:
                    cubes_to_keep_on.append(current_box)
            current_on_cubes = cubes_to_keep_on
    return sum(b.volume() for b in current_on_cubes)


def part_1() -> None:
    print(run_cubes())


def part_2() -> None:
    print(run_cubes(part_2=True))
