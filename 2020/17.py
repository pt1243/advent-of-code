from itertools import product

with open("./2020/resources/17.txt") as f:
    lines = f.read().splitlines()


def part_1() -> None:
    current: set[tuple[int, int, int]] = set()
    for x, line in enumerate(lines):
        for y, char in enumerate(line):
            if char == "#":
                current.add((x, y, 0))

    for _ in range(6):
        min_x = min(cube[0] for cube in current) - 1
        max_x = max(cube[0] for cube in current) + 1
        min_y = min(cube[1] for cube in current) - 1
        max_y = max(cube[1] for cube in current) + 1
        min_z = min(cube[2] for cube in current) - 1
        max_z = max(cube[2] for cube in current) + 1

        new: set[tuple[int, int, int]] = set()
        for x, y, z in product(range(min_x, max_x + 1), range(min_y, max_y + 1), range(min_z, max_z + 1)):
            neighbours = sum(
                1
                for dx, dy, dz in product(range(-1, 2), repeat=3)
                if (x + dx, y + dy, z + dz) in current and (dx, dy, dz) != (0, 0, 0)
            )
            if (x, y, z) in current:
                if neighbours == 2 or neighbours == 3:
                    new.add((x, y, z))
            else:
                if neighbours == 3:
                    new.add((x, y, z))
        current = new
    print(len(current))


def part_2() -> None:
    current: set[tuple[int, int, int, int]] = set()
    for x, line in enumerate(lines):
        for y, char in enumerate(line):
            if char == "#":
                current.add((x, y, 0, 0))

    for _ in range(6):
        min_x = min(cube[0] for cube in current) - 1
        max_x = max(cube[0] for cube in current) + 1
        min_y = min(cube[1] for cube in current) - 1
        max_y = max(cube[1] for cube in current) + 1
        min_z = min(cube[2] for cube in current) - 1
        max_z = max(cube[2] for cube in current) + 1
        min_w = min(cube[3] for cube in current) - 1
        max_w = max(cube[3] for cube in current) + 1

        new: set[tuple[int, int, int, int]] = set()
        for x, y, z, w in product(
            range(min_x, max_x + 1), range(min_y, max_y + 1), range(min_z, max_z + 1), range(min_w, max_w + 1)
        ):
            neighbours = sum(
                1
                for dx, dy, dz, dw in product(range(-1, 2), repeat=4)
                if (x + dx, y + dy, z + dz, w + dw) in current and (dx, dy, dz, dw) != (0, 0, 0, 0)
            )
            if (x, y, z, w) in current:
                if neighbours == 2 or neighbours == 3:
                    new.add((x, y, z, w))
            else:
                if neighbours == 3:
                    new.add((x, y, z, w))
        current = new
    print(len(current))
