import heapq
from collections import defaultdict

with open("./2019/resources/20.txt") as f:
    lines = f.read().splitlines()


def get_distances(lines: list[str]) -> defaultdict[str, dict[str, int]]:
    full_width, full_height = len(lines[0]), len(lines)
    top_outer_edge, bottom_outer_edge = 2, full_height - 3
    left_outer_edge, right_outer_edge = 2, full_width - 3
    vertical_midpoint, horizontal_midpoint = full_height // 2, full_width // 2

    vertical_line = "".join(line[horizontal_midpoint] for line in lines)
    top_vertical_line, bottom_vertical_line = vertical_line[:vertical_midpoint], vertical_line[vertical_midpoint:]
    horizontal_line = lines[vertical_midpoint]
    left_horizontal_line, right_horizontal_line = (
        horizontal_line[:horizontal_midpoint],
        horizontal_line[horizontal_midpoint:],
    )

    if "#" in top_vertical_line and "." in top_vertical_line:
        top_inner_edge = max(top_vertical_line.rindex("#"), top_vertical_line.rindex("."))
    elif "#" in top_vertical_line:
        top_inner_edge = top_vertical_line.rindex("#")
    else:
        top_inner_edge = top_vertical_line.rindex(".")

    bottom_inner_edge = len(top_vertical_line)
    if "#" in bottom_vertical_line and "." in bottom_vertical_line:
        bottom_inner_edge += min(bottom_vertical_line.index("#"), bottom_vertical_line.index("."))
    elif "#" in bottom_vertical_line:
        bottom_inner_edge += bottom_vertical_line.index("#")
    else:
        bottom_inner_edge += bottom_vertical_line.index(".")

    if "#" in left_horizontal_line and "." in left_horizontal_line:
        left_inner_edge = max(left_horizontal_line.rindex("#"), left_horizontal_line.rindex("."))
    elif "#" in left_horizontal_line:
        left_inner_edge = left_horizontal_line.rindex("#")
    else:
        left_inner_edge = left_horizontal_line.rindex(".")

    right_inner_edge = len(left_horizontal_line)
    if "#" in right_horizontal_line and "." in right_horizontal_line:
        right_inner_edge += min(right_horizontal_line.index("#"), right_horizontal_line.index("."))
    elif "#" in right_horizontal_line:
        right_inner_edge += right_horizontal_line.index("#")
    else:
        right_inner_edge += right_horizontal_line.index(".")

    top_outer_edge_positions = {(top_outer_edge, col) for col in range(left_outer_edge, right_outer_edge + 1)}
    bottom_outer_edge_positions = {(bottom_outer_edge, col) for col in range(left_outer_edge, right_outer_edge + 1)}
    left_outer_edge_positions = {(row, left_outer_edge) for row in range(top_outer_edge, bottom_outer_edge + 1)}
    right_outer_edge_positions = {(row, right_outer_edge) for row in range(top_outer_edge, bottom_outer_edge + 1)}
    top_inner_edge_positions = {(top_inner_edge, col) for col in range(left_inner_edge + 1, right_inner_edge)}
    bottom_inner_edge_positions = {(bottom_inner_edge, col) for col in range(left_inner_edge + 1, right_inner_edge)}
    left_inner_edge_positions = {(row, left_inner_edge) for row in range(top_inner_edge + 1, bottom_inner_edge)}
    right_inner_edge_positions = {(row, right_inner_edge) for row in range(top_inner_edge + 1, bottom_inner_edge)}

    outer_edge_positions = (
        top_outer_edge_positions | bottom_outer_edge_positions | left_outer_edge_positions | right_outer_edge_positions
    )
    inner_edge_positions = (
        top_inner_edge_positions | bottom_inner_edge_positions | left_inner_edge_positions | right_inner_edge_positions
    )
    all_positions = outer_edge_positions | inner_edge_positions

    def read_label(pos: tuple[int, int]) -> str:
        row, col = pos
        if pos in top_outer_edge_positions or pos in bottom_inner_edge_positions:
            connection = lines[row - 2][col] + lines[row - 1][col]
        elif pos in bottom_outer_edge_positions or pos in top_inner_edge_positions:
            connection = lines[row + 1][col] + lines[row + 2][col]
        elif pos in left_outer_edge_positions or pos in right_inner_edge_positions:
            connection = lines[row][col - 2] + lines[row][col - 1]
        elif pos in right_outer_edge_positions or pos in left_inner_edge_positions:
            connection = lines[row][col + 1] + lines[row][col + 2]
        else:
            raise ValueError("position is not along an edge")
        suffix = "" if connection in ("AA", "ZZ") else ("_outer" if pos in outer_edge_positions else "_inner")
        return connection + suffix

    distances: defaultdict[str, dict[str, int]] = defaultdict(dict)
    offsets = ((-1, 0), (0, 1), (1, 0), (0, -1))
    for pos in all_positions:
        if lines[pos[0]][pos[1]] == ".":
            starting_label = read_label(pos)
            current_distances = distances[starting_label]
            spaces_to_check: list[tuple[tuple[int, int], int, set[tuple[int, int]]]] = []
            for offset in offsets:
                starting_position = (pos[0] + offset[0], pos[1] + offset[1])
                if lines[starting_position[0]][starting_position[1]] == ".":
                    spaces_to_check.append((starting_position, 1, {pos, starting_position}))
            while spaces_to_check:
                current_position, dist, seen = spaces_to_check.pop()
                if current_position in all_positions:
                    label = read_label(current_position)
                    if label not in current_distances:
                        current_distances[label] = dist
                    else:
                        current_distances[label] = min(current_distances[label], dist)
                    continue
                for offset in offsets:
                    new_position = (current_position[0] + offset[0], current_position[1] + offset[1])
                    if lines[new_position[0]][new_position[1]] == "." and new_position not in seen:
                        new_seen = seen.copy()
                        new_seen.add(current_position)
                        spaces_to_check.append((new_position, dist + 1, new_seen))
    return distances


def part_1() -> None:
    distances = get_distances(lines)
    paths_to_check: list[tuple[int, str]] = [(0, "AA")]
    while paths_to_check:
        dist, current = heapq.heappop(paths_to_check)
        if current == "ZZ":
            print(dist)
            return
        for neighbour, dist_to_neighbour in distances[current].items():
            if neighbour in ("AA", "ZZ"):  # skip moving from inside to outside
                new_current = neighbour
                new_dist = dist + dist_to_neighbour
            else:
                new_current, suffix = neighbour.split("_")
                new_suffix = "_inner" if suffix == "outer" else "_outer"
                new_current += new_suffix
                new_dist = dist + dist_to_neighbour + 1
            heapq.heappush(paths_to_check, (new_dist, new_current))


def part_2() -> None:
    distances = get_distances(lines)
    paths_to_check: list[tuple[int, str, int]] = [(0, "AA", 0)]
    while paths_to_check:
        dist, current, depth = heapq.heappop(paths_to_check)
        if current == "ZZ" and depth == 0:
            print(dist)
            return
        for neighbour, dist_to_neighbour in distances[current].items():
            if neighbour in ("AA", "ZZ"):
                if depth != 0:
                    continue
                new_current = neighbour
                new_dist = dist + dist_to_neighbour
                new_depth = 0
            else:
                new_current, suffix = neighbour.split("_")
                if depth == 0 and suffix == "outer":
                    continue
                new_suffix = "_inner" if suffix == "outer" else "_outer"
                new_current += new_suffix
                new_dist = dist + dist_to_neighbour + 1
                new_depth = depth + (1 if suffix == "inner" else -1)
            heapq.heappush(paths_to_check, (new_dist, new_current, new_depth))
