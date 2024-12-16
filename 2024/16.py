from collections import defaultdict
import heapq


with open("./2024/resources/16.txt") as f:
    lines = f.read().splitlines()


def a_star(start_row: int, start_col: int, start_direction: int) -> int:
    end_row = next(i for i, line in enumerate(lines) if "E" in line)
    end_col = lines[end_row].index("E")
    directions = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}

    open_set = [(0, start_row, start_col, start_direction)]

    g_score: defaultdict[tuple[int, int, int], int] = defaultdict(lambda: 10**12)
    g_score[start_row, start_col, start_direction] = 0
    f_score: defaultdict[tuple[int, int, int], int] = defaultdict(lambda: 10**12)
    f_score[start_row, start_col, start_direction] = abs(start_row - end_row) + abs(start_col - end_col)

    while open_set:
        _, row, col, direction = heapq.heappop(open_set)
        if row == end_row and col == end_col:
            return g_score[row, col, direction]
        for new_direction, (drow, dcol) in directions.items():
            if (direction + 2) % 4 == new_direction and row != start_row and col != start_col:
                continue
            new_row = row + drow
            new_col = col + dcol
            if lines[new_row][new_col] == "#":
                continue
            tentative_g_score = (
                g_score[row, col, direction]
                + 1
                + (2000 if (direction + 2) % 4 == new_direction else (1000 if direction != new_direction else 0))
            )
            if tentative_g_score < g_score[new_row, new_col, new_direction]:
                g_score[new_row, new_col, new_direction] = tentative_g_score
                f_score[new_row, new_col, new_direction] = (
                    tentative_g_score + abs(new_row - end_row) + abs(new_col - end_col)
                )
                heapq.heappush(open_set, (f_score[new_row, new_col, new_direction], new_row, new_col, new_direction))
    raise ValueError("did not find path")


def problem_1() -> None:
    start_row = next(i for i, line in enumerate(lines) if "S" in line)
    start_col = lines[start_row].index("S")
    print(a_star(start_row, start_col, 1))


def problem_2() -> None:
    start_row = next(i for i, line in enumerate(lines) if "S" in line)
    start_col = lines[start_row].index("S")
    best_path_cost = a_star(start_row, start_col, 1)
    end_row = next(i for i, line in enumerate(lines) if "E" in line)
    end_col = lines[end_row].index("E")
    directions = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}

    intersections: dict[tuple[int, int], list[int]] = {}
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == "#":
                continue
            connections: list[int] = []
            for direction, (drow, dcol) in directions.items():
                if lines[row + drow][col + dcol] != "#":
                    connections.append(direction)
            if len(connections) != 2 or (connections[0] + 2) % 4 != connections[1]:
                intersections[row, col] = connections

    distances_between_intersections: dict[tuple[int, int], dict[int, int]] = {}
    for intersection, available_directions in intersections.items():
        results: dict[int, int] = {}
        for available_direction in available_directions:
            row, col = intersection
            drow, dcol = directions[available_direction]
            row += drow
            col += dcol
            dist = 1
            while (row, col) not in intersections:
                row += drow
                col += dcol
                dist += 1
            results[available_direction] = dist
        distances_between_intersections[intersection] = results

    costs_to_end: dict[tuple[int, int, int], int] = {}
    for (intersection_row, intersection_col) in distances_between_intersections:
        for i in range(4):
            costs_to_end[intersection_row, intersection_col, i] = a_star(intersection_row, intersection_col, i)
    for i in range(4):
        costs_to_end[end_row, end_col, i] = 0

    tiles_on_best_paths = {(start_row, start_col)}
    open_set: list[tuple[int, int, int, int, list[tuple[int, int, int]]]] = [(0, start_row, start_col, 1, [])]
    while open_set:
        score, row, col, direction, history = open_set.pop()
        if row == end_row and col == end_col:
            for row, col, direction in history:
                drow, dcol = directions[direction]
                tiles_on_best_paths.add((row, col))
                dist = distances_between_intersections[row, col][direction]
                for _ in range(dist):
                    row += drow
                    col += dcol
                    tiles_on_best_paths.add((row, col))
            continue
        for new_direction, dist in distances_between_intersections[row, col].items():
            if (direction + 2) % 4 == new_direction:
                continue
            new_score = score + dist + (1000 if new_direction != direction else 0)
            drow, dcol = directions[new_direction]
            new_row = row + drow * dist
            new_col = col + dcol * dist
            if new_score + costs_to_end[new_row, new_col, new_direction] > best_path_cost:
                continue
            open_set.append((new_score, new_row, new_col, new_direction, history + [(row, col, new_direction)]))

    print(len(tiles_on_best_paths))
