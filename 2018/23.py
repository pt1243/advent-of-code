import heapq
from itertools import product
from math import ceil, log2
from operator import itemgetter
from typing import NamedTuple, cast

with open("./2018/resources/23.txt") as f:
    lines = f.read().splitlines()


class Nanobot(NamedTuple):
    x: int
    y: int
    z: int
    r: int


def problem_1() -> None:
    nanobots: list[Nanobot] = []
    for line in lines:
        x, y, z = (int(n) for n in line[line.index("<") + 1 : line.index(">")].split(","))
        r = int(line[line.index("r=") + 2 :])
        nanobots.append(Nanobot(x, y, z, r))

    strongest = max(nanobots, key=itemgetter(3))
    num_in_range = 0
    for nanobot in nanobots:
        dist = abs(strongest.x - nanobot.x) + abs(strongest.y - nanobot.y) + abs(strongest.z - nanobot.z)
        if dist <= strongest.r:
            num_in_range += 1
    print(num_in_range)


def problem_2() -> None:
    nanobots: list[Nanobot] = []
    for line in lines:
        x, y, z = (int(n) for n in line[line.index("<") + 1 : line.index(">")].split(","))
        r = int(line[line.index("r=") + 2 :])
        nanobots.append(Nanobot(x, y, z, r))

    min_x = min(n.x - n.r for n in nanobots)
    max_x = max(n.x + n.r for n in nanobots)
    min_y = min(n.y - n.r for n in nanobots)
    max_y = max(n.y + n.r for n in nanobots)
    min_z = min(n.z - n.r for n in nanobots)
    max_z = max(n.z + n.r for n in nanobots)

    def intersect(box: tuple[int, int, int, int, int, int], bot: Nanobot) -> bool:
        box_low_x, box_high_x, box_low_y, box_high_y, box_low_z, box_high_z = box
        dist = 0
        if bot.x <= box_low_x:
            dist += box_low_x - bot.x
        if bot.x >= box_high_x:
            dist += bot.x - box_high_x
        if bot.y <= box_low_y:
            dist += box_low_y - bot.y
        if bot.y >= box_high_y:
            dist += bot.y - box_high_y
        if bot.z <= box_low_z:
            dist += box_low_z - bot.z
        if bot.z >= box_high_z:
            dist += bot.z - box_high_z
        return dist <= bot.r

    def min_possible_dist_to_origin(box: tuple[int, int, int, int, int, int]) -> int:
        box_low_x, box_high_x, box_low_y, box_high_y, box_low_z, box_high_z = box
        closest_x = min(abs(box_low_x), abs(box_high_x))
        closest_y = min(abs(box_low_y), abs(box_high_y))
        closest_z = min(abs(box_low_z), abs(box_high_z))
        return closest_x + closest_y + closest_z

    max_coord_dist = max(abs(dist) for dist in (min_x, max_x, min_y, max_y, min_z, max_z))
    starting_size = cast(int, 2 ** ceil(log2(max_coord_dist)))
    starting_box = (
        -starting_size + 1,
        starting_size,
        -starting_size + 1,
        starting_size,
        -starting_size + 1,
        starting_size,
    )
    boxes_to_check = [(-1000, min_possible_dist_to_origin(starting_box), 2 * starting_size, starting_box)]
    while boxes_to_check:
        _, dist_to_origin, size, box = heapq.heappop(boxes_to_check)
        min_x, _, min_y, _, min_z, _ = box
        if size == 1:
            print(dist_to_origin)
            return
        new_size = size // 2
        for x_axis_offset, y_axis_offset, z_axis_offset in product(range(2), repeat=3):
            new_min_x = min_x + x_axis_offset * new_size
            new_max_x = new_min_x + new_size - 1
            new_min_y = min_y + y_axis_offset * new_size
            new_max_y = new_min_y + new_size - 1
            new_min_z = min_z + z_axis_offset * new_size
            new_max_z = new_min_z + new_size - 1
            new_box = (new_min_x, new_max_x, new_min_y, new_max_y, new_min_z, new_max_z)
            new_num_in_range = sum(1 for bot in nanobots if intersect(new_box, bot))
            if new_num_in_range:
                heapq.heappush(
                    boxes_to_check, (-new_num_in_range, min_possible_dist_to_origin(new_box), new_size, new_box)
                )
