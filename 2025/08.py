from __future__ import annotations

from itertools import combinations
from math import prod
from typing import NamedTuple

with open("./2025/resources/8.txt") as f:
    lines = f.read().splitlines()


class Junction(NamedTuple):
    x: int
    y: int
    z: int

    def distance(self, other: Junction) -> float:
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2


def part_1() -> None:
    junctions = [Junction(*map(int, line.split(","))) for line in lines]
    distances: list[tuple[float, Junction, Junction]] = []

    for junction_1, junction_2 in combinations(junctions, 2):
        distances.append((junction_1.distance(junction_2), junction_1, junction_2))
    distances.sort()

    next_circuit_number = 0
    circuit_sizes: dict[int, int] = {}
    junction_circuits: dict[Junction, int] = {}

    for _, junction_1, junction_2 in distances[:1000]:
        circuit_1 = junction_circuits.get(junction_1, None)
        circuit_2 = junction_circuits.get(junction_2, None)
        if circuit_1 is None and circuit_2 is None:
            junction_circuits[junction_1] = next_circuit_number
            junction_circuits[junction_2] = next_circuit_number
            circuit_sizes[next_circuit_number] = 2
            next_circuit_number += 1
        elif circuit_1 is None:
            junction_circuits[junction_1] = junction_circuits[junction_2]
            circuit_sizes[junction_circuits[junction_2]] += 1
        elif circuit_2 is None:
            junction_circuits[junction_2] = junction_circuits[junction_1]
            circuit_sizes[junction_circuits[junction_1]] += 1
        else:
            if junction_circuits[junction_1] == junction_circuits[junction_2]:
                continue
            to_merge = [junction for junction, circuit in junction_circuits.items() if circuit == circuit_2]
            for junction in to_merge:
                junction_circuits[junction] = circuit_1
            del circuit_sizes[circuit_2]
            circuit_sizes[circuit_1] += len(to_merge)

    print(prod(sorted(circuit_sizes.values())[-3:]))


def part_2() -> None:
    points = [Junction(*map(int, line.split(","))) for line in lines]
    distances: list[tuple[float, Junction, Junction]] = []

    for junction_1, junction_2 in combinations(points, 2):
        distances.append((junction_1.distance(junction_2), junction_1, junction_2))
    distances.sort()

    next_circuit_number = 0
    circuit_sizes: dict[int, int] = {}
    junction_circuits: dict[Junction, int] = {}
    circuit_count = 0

    for _, junction_1, junction_2 in distances:
        circuit_1 = junction_circuits.get(junction_1, None)
        circuit_2 = junction_circuits.get(junction_2, None)
        if circuit_1 is None and circuit_2 is None:
            junction_circuits[junction_1] = next_circuit_number
            junction_circuits[junction_2] = next_circuit_number
            circuit_sizes[next_circuit_number] = 2
            next_circuit_number += 1
            circuit_count += 1
        elif circuit_1 is None:
            junction_circuits[junction_1] = junction_circuits[junction_2]
            circuit_sizes[junction_circuits[junction_2]] += 1
        elif circuit_2 is None:
            junction_circuits[junction_2] = junction_circuits[junction_1]
            circuit_sizes[junction_circuits[junction_1]] += 1
        else:
            if junction_circuits[junction_1] == junction_circuits[junction_2]:
                continue
            to_merge = [junction for junction, circuit in junction_circuits.items() if circuit == circuit_2]
            for junction in to_merge:
                junction_circuits[junction] = circuit_1
            del circuit_sizes[circuit_2]
            circuit_count -= 1
            circuit_sizes[circuit_1] += len(to_merge)
        if circuit_count == 1 and next(circuit_size for circuit_size in circuit_sizes.values()) == 1000:
            print(junction_1.x * junction_2.x)
            return
