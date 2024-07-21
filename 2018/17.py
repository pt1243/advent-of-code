from collections import defaultdict
import sys


sys.setrecursionlimit(10_000)

with open("./2018/resources/17.txt") as f:
    lines = [line.strip() for line in f]


def fill(x: int, y: int, tiles: defaultdict[tuple[int, int], str], max_y: int) -> defaultdict[tuple[int, int], str]:
    solid_tiles = ("#", "~")
    tiles[(x, y)] = "|"
    while tiles[(x, y + 1)] not in solid_tiles:
        if tiles[(x, y + 1)] == "|":
            return tiles
        y += 1
        tiles[(x, y)] = "|"
        if y > max_y:
            return tiles
    original_x = x
    while tiles[(x, y + 1)] in solid_tiles and tiles[(x - 1, y)] != "#":  # move left as far as possible
        x -= 1
        tiles[(x, y)] = "|"
    left_edge_contained = False
    if tiles[(x, y + 1)] not in solid_tiles:  # check if we can move down; if so, call recursively
        fill(x, y, tiles, max_y)
    else:  # mark left edge as solid
        left_x = x
        left_edge_contained = True
    x = original_x
    while tiles[(x, y + 1)] in solid_tiles and tiles[(x + 1, y)] != "#":  # move right as far as possible
        x += 1
        if tiles[(x, y)] != "~":
            tiles[(x, y)] = "|"
    if tiles[(x, y + 1)] not in solid_tiles:
        fill(x, y, tiles, max_y)
    else:
        if left_edge_contained:
            for col in range(left_x, x + 1):
                tiles[(col, y)] = "~"
            fill(original_x, y - 1, tiles, max_y)
    return tiles


def problem_1() -> None:
    tiles: defaultdict[tuple[int, int], str] = defaultdict(lambda: ".")
    for line in lines:
        left, right = line.split(", ")
        left_num = int(left[2:])
        right_start, right_end = (int(val) for val in right[2:].split(".."))
        left_is_x = left[0] == "x"
        for i in range(right_start, right_end + 1):
            if left_is_x:
                tiles[(left_num, i)] = "#"
            else:
                tiles[(i, left_num)] = "#"
    min_y = min(pos[1] for pos in tiles.keys())
    max_y = max(pos[1] for pos in tiles.keys())

    tiles = fill(500, 0, tiles, max_y)
    print(sum(1 for (_, y), tile in tiles.items() if tile in ("|", "~") and min_y <= y <= max_y))


def problem_2() -> None:
    tiles: defaultdict[tuple[int, int], str] = defaultdict(lambda: ".")
    for line in lines:
        left, right = line.split(", ")
        left_num = int(left[2:])
        right_start, right_end = (int(val) for val in right[2:].split(".."))
        left_is_x = left[0] == "x"
        for i in range(right_start, right_end + 1):
            if left_is_x:
                tiles[(left_num, i)] = "#"
            else:
                tiles[(i, left_num)] = "#"
    min_y = min(pos[1] for pos in tiles.keys())
    max_y = max(pos[1] for pos in tiles.keys())

    tiles = fill(500, 0, tiles, max_y)
    print(sum(1 for (_, y), tile in tiles.items() if tile == "~" and min_y <= y <= max_y))
