import heapq
from collections import defaultdict

with open("./2016/resources/13.txt") as f:
    designer_number = int(f.read().strip())


def is_open(node: tuple[int, int]) -> bool:
    x, y = node
    return (x * x + 3 * x + 2 * x * y + y + y * y + designer_number).bit_count() % 2 == 0


def get_neighbours(node: tuple[int, int]) -> list[tuple[int, int]]:
    x, y = node
    tentative_neighbours = [(x, y + 1), (x + 1, y)]
    if x != 0:
        tentative_neighbours.append((x - 1, y))
    if y != 0:
        tentative_neighbours.append((x, y - 1))
    return [n for n in tentative_neighbours if is_open(n)]


def a_star(start: tuple[int, int], goal: tuple[int, int]) -> list[tuple[int, int]]:
    # list of nodes visited to get to the goal
    def reconstruct_path(current: tuple[int, int]) -> list[tuple[int, int]]:
        total_path: list[tuple[int, int]] = [current]
        while current in came_from:
            current = came_from[current]
            total_path.append(current)
        return list(reversed(total_path))

    # heuristic function: Manhattan distance
    def h(node: tuple[int, int], goal: tuple[int, int]) -> int:
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

    open_set: list[tuple[int, int, int]] = [(0, *start)]  # num steps, x, y
    open_set_set = {start}
    came_from: dict[tuple[int, int], tuple[int, int]] = {}

    g_score: defaultdict[tuple[int, int], int] = defaultdict(lambda: 10**6)
    g_score[start] = 0

    f_score: defaultdict[tuple[int, int], int] = defaultdict(lambda: 10**6)
    f_score[start] = h(start, goal)

    while open_set:
        _, x, y = heapq.heappop(open_set)
        current = (x, y)
        open_set_set.remove(current)
        if current == goal:
            return reconstruct_path(current)
        for neighbor in get_neighbours(current):
            tentative_g_score = g_score[current] + 1  # one more step
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + h(neighbor, goal)
                if neighbor not in open_set_set:
                    open_set_set.add(neighbor)
                    heapq.heappush(open_set, (tentative_g_score, neighbor[0], neighbor[1]))
    raise ValueError("did not find path to goal")


def part_1() -> None:
    target = (31, 39)
    print(len(a_star((1, 1), target)) - 1)


def part_2() -> None:
    visited: set[tuple[int, int]] = {(1, 1)}
    for _ in range(50):
        for start_node in visited.copy():
            for neighbour in get_neighbours(start_node):
                visited.add(neighbour)
    print(len(visited))
