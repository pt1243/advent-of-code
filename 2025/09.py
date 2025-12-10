from itertools import combinations, count, pairwise

from more_itertools import intersperse

with open("./2025/resources/9.txt") as f:
    lines = f.read().splitlines()


def part_1() -> None:
    positions = [tuple(map(int, line.split(","))) for line in lines]
    print(max((abs(r1[0] - r2[0]) + 1) * (abs(r1[1] - r2[1]) + 1) for r1, r2 in combinations(positions, 2)))


def part_2() -> None:
    positions = [tuple(map(int, line.split(","))) for line in lines]

    # construct edges of the rectangle
    # vertical edges are stored as a tuple of (horizontal position, lower, upper)
    # horizontal edges are stored as a tuple of (vertical position, left, right)
    vertical_edges: list[tuple[int, int, int]] = []
    horizontal_edges: list[tuple[int, int, int]] = []

    # we may have a rectangle that does not intersect with any edges, but who has one corner outside the filled area
    # compress the coordinates to do a floodfill of the outside points
    x_compression: dict[int, int] = {}
    y_compression: dict[int, int] = {}
    for x, i in zip(intersperse(None, sorted(set(p[0] for p in positions))), count()):
        if x is None:
            continue
        x_compression[x] = i
    for y, i in zip(intersperse(None, sorted(set(p[1] for p in positions))), count()):
        if y is None:
            continue
        y_compression[y] = i

    compressed_edge_points: set[tuple[int, int]] = set()
    for p1, p2 in pairwise(positions + [positions[0]]):
        if p1[0] == p2[0]:  # same horizontal position: vertical edge
            y1 = min(p1[1], p2[1])
            y2 = max(p1[1], p2[1])
            vertical_edges.append((p1[0], y1, y2))
            for y in range(y_compression[y1], y_compression[y2] + 1):
                compressed_edge_points.add((x_compression[p1[0]], y))
        else:  # same vertical position: horizontal edge
            x1 = min(p1[0], p2[0])
            x2 = max(p1[0], p2[0])
            horizontal_edges.append((p1[1], x1, x2))
            for x in range(x_compression[x1], x_compression[x2] + 1):
                compressed_edge_points.add((x, y_compression[p1[1]]))

    min_x = min(x_compression.values()) - 1
    max_x = max(x_compression.values()) + 1
    min_y = min(y_compression.values()) - 1
    max_y = max(y_compression.values()) + 1

    outside_points: set[tuple[int, int]] = set()
    open_set = [(max_x, max_y)]  # definitely outside
    while open_set:
        current = open_set.pop()
        outside_points.add(current)
        for dx, dy in ((-1, 0), (0, 1), (1, 0), (0, -1)):
            new = (current[0] + dx, current[1] + dy)
            if (
                min_x <= new[0] <= max_x
                and min_y <= new[1] <= max_y
                and new not in outside_points
                and new not in compressed_edge_points
            ):
                open_set.append(new)

    for corner_1, corner_2 in sorted(
        combinations(positions, 2),
        key=lambda corner_pair: (
            (abs(corner_pair[0][0] - corner_pair[1][0]) + 1) * (abs(corner_pair[0][1] - corner_pair[1][1]) + 1)
        ),
        reverse=True,
    ):
        # check that the other two corners are not in outside points
        if (x_compression[corner_1[0]], y_compression[corner_2[1]]) in outside_points or (
            x_compression[corner_2[0]],
            y_compression[corner_1[1]],
        ) in outside_points:
            continue

        # check if any edges intersect the rectangle
        top_edge_location = max(corner_1[1], corner_2[1])
        bottom_edge_location = min(corner_1[1], corner_2[1])
        left_edge_location = min(corner_1[0], corner_2[0])
        right_edge_location = max(corner_1[0], corner_2[0])
        if any(
            left_edge_location < position < right_edge_location
            and (lower < top_edge_location < upper or lower < bottom_edge_location < upper)
            for position, lower, upper in vertical_edges
        ) or any(
            bottom_edge_location < position < top_edge_location
            and (lower < left_edge_location < upper or lower < right_edge_location < upper)
            for position, lower, upper in horizontal_edges
        ):
            continue
        print((abs(corner_1[0] - corner_2[0]) + 1) * (abs(corner_1[1] - corner_2[1]) + 1))
        return
