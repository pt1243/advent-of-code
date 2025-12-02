import heapq
from collections import defaultdict

with open("./2023/resources/17.txt") as f:
    heat_map = [[int(char) for char in line] for line in f.read().splitlines()]


def a_star(min_dist: int, max_dist: int) -> int:
    open_set = [(0, (0, 0, 1)), (0, (0, 0, 2))]

    height, width = len(heat_map), len(heat_map[0])
    target = (height - 1, width - 1)
    directions = ((-1, 0), (0, 1), (1, 0), (0, -1))

    g_score: defaultdict[tuple[int, int, int], int] = defaultdict(lambda: 10**12)
    g_score[0, 0, 1] = 0
    g_score[0, 0, 2] = 0
    f_score: defaultdict[tuple[int, int, int], int] = defaultdict(lambda: 10**12)
    starting_dist = target[0] + target[1]
    f_score[0, 0, 1] = starting_dist
    f_score[0, 0, 2] = starting_dist

    while open_set:
        _, (row, col, direction) = heapq.heappop(open_set)
        if (row, col) == target:
            return g_score[row, col, direction]
        drow, dcol = directions[direction]

        possible_neighbours: list[tuple[int, tuple[int, int, int]]] = []
        for dist_moved in range(min_dist, max_dist + 1):
            new_row, new_col = row + drow * dist_moved, col + dcol * dist_moved
            if not (0 <= new_row < height and 0 <= new_col < width):
                continue
            possible_neighbours.append((dist_moved, (new_row, new_col, (direction - 1) % 4)))
            possible_neighbours.append((dist_moved, (new_row, new_col, (direction + 1) % 4)))

        current_g_score = g_score[row, col, direction]
        for dist_moved, neighbour in possible_neighbours:
            spaces_encountered = [(row + drow * moved, col + dcol * moved) for moved in range(1, dist_moved + 1)]
            heat_loss = sum(heat_map[r][c] for (r, c) in spaces_encountered)
            tentative_g_score = current_g_score + heat_loss
            if tentative_g_score < g_score[neighbour]:
                g_score[neighbour] = tentative_g_score
                f_score[neighbour] = tentative_g_score + abs(neighbour[0] - target[0]) + abs(neighbour[1] - target[1])
                heapq.heappush(open_set, (f_score[neighbour], neighbour))
    raise ValueError("could not reach target")


def part_1() -> None:
    print(a_star(1, 3))


def part_2() -> None:
    print(a_star(4, 10))
