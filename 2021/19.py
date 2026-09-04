from itertools import combinations, product
from typing import NamedTuple

with open("./2021/resources/19.txt") as f:
    lines = f.read().strip()


class Vec(NamedTuple):
    x: int
    y: int
    z: int

    def cross(self, other: Vec):
        return Vec(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def within_range(self, other: Vec) -> bool:
        return abs(self.x - other.x) <= 1000 and abs(self.y - other.y) <= 1000 and abs(self.z - other.z) <= 1000

    def manhattan_distance(self, other: Vec) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    # overriding these tuple methods is technically unsafe, but it's worth it for the tuple performance over dataclasses
    def __add__(self, value: Vec) -> Vec:  # ty: ignore[invalid-method-override]
        return Vec(self.x + value.x, self.y + value.y, self.z + value.z)

    def __sub__(self, other: Vec) -> Vec:
        return Vec(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, value: int) -> Vec:  # ty: ignore[invalid-method-override]
        return Vec(self.x * value, self.y * value, self.z * value)


class Rotation(NamedTuple):
    x_basis: Vec
    y_basis: Vec
    z_basis: Vec

    def __matmul__(self, value: Vec) -> Vec:
        return Vec(
            self.x_basis.x * value.x + self.y_basis.x * value.y + self.z_basis.x * value.z,
            self.x_basis.y * value.x + self.y_basis.y * value.y + self.z_basis.y * value.z,
            self.x_basis.z * value.x + self.y_basis.z * value.y + self.z_basis.z * value.z,
        )


def solve_beacon_map() -> tuple[int, list[Vec]]:
    x, y, z = Vec(1, 0, 0), Vec(0, 1, 0), Vec(0, 0, 1)
    bases: list[Rotation] = []
    for v1, sign1, v2, sign2 in product((x, y, z), (1, -1), (x, y, z), (1, -1)):
        if v1 == v2:
            continue
        x_basis = v1 * sign1
        y_basis = v2 * sign2
        bases.append(Rotation(x_basis, y_basis, x_basis.cross(y_basis)))

    scanner_blocks = lines.split("\n\n")
    confirmed_scanners = [Vec(0, 0, 0)]
    confirmed_beacon_sets = [[Vec(*map(int, line.split(","))) for line in scanner_blocks[0].splitlines()[1:]]]
    beacon_sets_to_check = [
        [Vec(*map(int, line.split(","))) for line in block.splitlines()[1:]] for block in scanner_blocks[1:]
    ]

    def check_for_scanner_overlap(
        existing_beacon_set: list[Vec], candidate_beacon_set: list[Vec]
    ) -> tuple[Vec, list[Vec]] | None:
        for base in bases:
            reoriented = {base @ b for b in candidate_beacon_set}
            for existing_beacon in existing_beacon_set:
                for candidate_beacon in reoriented:
                    # assuming that the given beacon is the same between sets, compute the scanner position
                    scanner_pos = existing_beacon - candidate_beacon
                    match_count = 0
                    for other_existing_beacon in existing_beacon_set:
                        # check if the existing beacon is within range of the scanner
                        if other_existing_beacon.within_range(scanner_pos):
                            expected_relative_location = other_existing_beacon - scanner_pos
                            if expected_relative_location in reoriented:
                                match_count += 1
                            else:
                                break
                        else:
                            pass  # outside scanner range, ignore
                    if match_count >= 12:
                        # we have confirmed the location and orientation of the scanner; compute the absolute positions
                        # of the candidate beacons
                        return scanner_pos, [scanner_pos + b for b in reoriented]
        return None

    while beacon_sets_to_check:
        for candidate_beacon_set in beacon_sets_to_check:
            for existing_beacon_set in confirmed_beacon_sets:
                if res := check_for_scanner_overlap(existing_beacon_set, candidate_beacon_set):
                    scanner_pos, beacon_positions = res
                    confirmed_scanners.append(scanner_pos)
                    break
            else:
                continue  # no existing beacon set matched - try a different candidate
            confirmed_beacon_sets.append(beacon_positions)
            break
        beacon_sets_to_check.remove(candidate_beacon_set)
    all_beacons = {b for blist in confirmed_beacon_sets for b in blist}
    return len(all_beacons), confirmed_scanners


def part_1() -> None:
    num_beacons, _ = solve_beacon_map()
    print(num_beacons)


def part_2() -> None:
    _, scanner_locations = solve_beacon_map()
    print(max(s1.manhattan_distance(s2) for s1, s2 in combinations(scanner_locations, 2)))
