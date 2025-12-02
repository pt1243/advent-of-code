from itertools import product
from typing import cast

with open("./2022/resources/18.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    cubes: set[tuple[int, int, int]] = set()
    for line in lines:
        cubes.add(cast(tuple[int, int, int], tuple(int(x) for x in line.split(","))))

    surface_area = 0
    for x, y, z in cubes:
        surface_area += (
            ((x - 1, y, z) not in cubes)
            + ((x + 1, y, z) not in cubes)
            + ((x, y - 1, z) not in cubes)
            + ((x, y + 1, z) not in cubes)
            + ((x, y, z - 1) not in cubes)
            + ((x, y, z + 1) not in cubes)
        )
    print(surface_area)


def problem_2() -> None:
    cubes: set[tuple[int, int, int]] = set()
    for line in lines:
        cubes.add(cast(tuple[int, int, int], tuple(int(x) for x in line.split(","))))

    min_x = min(cube[0] for cube in cubes)
    max_x = max(cube[0] for cube in cubes)
    min_y = min(cube[1] for cube in cubes)
    max_y = max(cube[1] for cube in cubes)
    min_z = min(cube[2] for cube in cubes)
    max_z = max(cube[2] for cube in cubes)

    air_inside: set[tuple[int, int, int]] = set()

    def mark_reachable(start_x: int, start_y: int, start_z: int) -> None:
        nonlocal air_inside
        open_set = [(start_x, start_y, start_z)]
        to_add: set[tuple[int, int, int]] = set()

        while open_set:
            x, y, z = open_set.pop()
            if x <= min_x - 1 or x >= max_x + 1 or y <= min_y - 1 or y >= max_y + 1 or z <= min_z - 1 or z >= max_z + 1:
                return
            to_add.add((x, y, z))
            for dx, dy, dz in ((-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)):
                neighbour = (x + dx, y + dy, z + dz)
                if neighbour not in to_add and neighbour not in cubes:
                    open_set.append(neighbour)
        air_inside |= to_add

    for x, y, z in product(range(min_x, max_x + 1), range(min_y, max_y + 1), range(min_z, max_z + 1)):
        if (x, y, z) not in cubes:
            mark_reachable(x, y, z)

    surfaces = cubes | air_inside
    exterior_surface_area = 0
    for x, y, z in cubes:
        exterior_surface_area += (
            ((x - 1, y, z) not in surfaces)
            + ((x + 1, y, z) not in surfaces)
            + ((x, y - 1, z) not in surfaces)
            + ((x, y + 1, z) not in surfaces)
            + ((x, y, z - 1) not in surfaces)
            + ((x, y, z + 1) not in surfaces)
        )
    print(exterior_surface_area)
