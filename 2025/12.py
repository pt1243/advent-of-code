from math import prod, sumprod

with open("./2025/resources/12.txt") as f:
    lines = f.read().strip()


def part_1() -> None:
    shapes, areas = lines.rsplit("\n\n", maxsplit=1)
    shape_sizes = [shape.count("#") for shape in shapes.split("\n\n")]
    total = 0
    for line in areas.split("\n"):
        left, right = line.split(": ")
        area = prod(map(int, left.split("x")))
        required = map(int, right.split())
        total += sumprod(required, shape_sizes) < area
    print(total)
