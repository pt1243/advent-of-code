from collections import defaultdict

with open("./2023/resources/23.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    max_path_length = 0
    current_paths: list[tuple[int, int, set[tuple[int, int]]]] = [(0, lines[0].index("."), set())]
    slopes = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}
    while current_paths:
        row, col, visited = current_paths.pop()
        if row == len(lines) - 1:
            max_path_length = max(max_path_length, len(visited))
            continue
        char = lines[row][col]
        if char != ".":
            drow, dcol = slopes[char]
            visited.add((row, col))
            current_paths.append((row + drow, col + dcol, visited))
        else:
            for drow, dcol in slopes.values():
                new_row, new_col = row + drow, col + dcol
                if new_row >= 0 and lines[new_row][new_col] != "#" and (new_row, new_col) not in visited:
                    char = lines[new_row][new_col]
                    if (
                        (char == "<" and dcol == 1)
                        or (char == ">" and dcol == -1)
                        or (char == "^" and drow == 1)
                        or (char == "v" and drow == -1)
                    ):
                        continue
                    new_visited = visited.copy()
                    new_visited.add((row, col))
                    current_paths.append((new_row, new_col, new_visited))
    print(max_path_length)


def problem_2() -> None:
    nodes: set[tuple[int, int]] = set()
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if row == 0 or row == len(lines) - 1 or char == "#":
                continue
            neighbour_indices = ((row - 1, col), (row, col + 1), (row + 1, col), (row, col - 1))
            if len([index for index in neighbour_indices if lines[index[0]][index[1]] != "#"]) != 2:
                nodes.add((row, col))
    start = (0, lines[0].index("."))
    end = (len(lines) - 1, lines[-1].index("."))
    nodes.add(start)
    nodes.add(end)

    def distance_between(starting_point: tuple[int, int], ending_point: tuple[int, int]) -> int:
        current: list[tuple[tuple[int, int], tuple[int, int], int]] = []
        offsets = ((-1, 0), (0, 1), (1, 0), (0, -1))
        max_dist = 0
        for offset in offsets:
            new_row, new_col = starting_point[0] + offset[0], starting_point[1] + offset[1]
            if 0 <= new_row < len(lines) and lines[new_row][new_col] != "#":
                current.append(((new_row, new_col), (starting_point[0], starting_point[1]), 1))
        while current:
            position, last_position, dist = current.pop()
            if position == ending_point:
                max_dist = max(max_dist, dist)
            if position in nodes or position[0] == 0 or position[0] == len(lines) - 1:
                continue
            for offset in offsets:
                new_position = (position[0] + offset[0], position[1] + offset[1])
                if new_position != last_position and lines[new_position[0]][new_position[1]] != "#":
                    current.append((new_position, position, dist + 1))
        return max_dist

    distances: defaultdict[tuple[int, int], dict[tuple[int, int], int]] = defaultdict(dict)
    for point in nodes:
        for other_point in nodes:
            dist = distance_between(point, other_point)
            if dist:
                distances[point][other_point] = dist
                distances[other_point][point] = dist

    paths: list[tuple[tuple[int, int], set[tuple[int, int]], int]] = [(start, set(), 0)]
    max_length = 0
    while paths:
        current_pos, visited, dist = paths.pop()
        if current_pos == end:
            max_length = max(max_length, dist)
            continue
        for neighbour, dist_to_neighbour in distances[current_pos].items():
            if neighbour not in visited:
                new_visited = visited.copy()
                new_visited.add(current_pos)
                paths.append((neighbour, new_visited, dist + dist_to_neighbour))
    print(max_length)
