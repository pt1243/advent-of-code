import heapq
from collections import defaultdict

with open("./2019/resources/18.txt") as f:
    lines = f.read().splitlines()


def get_distances(lines: list[str]) -> defaultdict[str, dict[str, int]]:
    offsets = ((-1, 0), (0, 1), (1, 0), (0, -1))
    distances: defaultdict[str, dict[str, int]] = defaultdict(dict)
    for row, line in enumerate(lines):
        for col, starting_char in enumerate(line):
            if starting_char not in ".#":
                current_distances = distances[starting_char]
                paths_to_check: list[tuple[tuple[int, int], int, set[tuple[int, int]]]] = []
                for offset in offsets:
                    starting_position = (row + offset[0], col + offset[1])
                    if lines[starting_position[0]][starting_position[1]] != "#":
                        paths_to_check.append((starting_position, 1, {(row, col), starting_position}))
                while paths_to_check:
                    current_position, dist, seen = paths_to_check.pop()
                    char = lines[current_position[0]][current_position[1]]
                    if char.isalpha():
                        if char not in current_distances:
                            current_distances[char] = dist
                        current_distances[char] = min(current_distances[char], dist)
                        continue
                    for offset in offsets:
                        new_position = (current_position[0] + offset[0], current_position[1] + offset[1])
                        if lines[new_position[0]][new_position[1]] != "#" and new_position not in seen:
                            new_seen = seen.copy()
                            new_seen.add(current_position)
                            paths_to_check.append((new_position, dist + 1, new_seen))
    return distances


def problem_1() -> None:
    distances = get_distances(lines)
    all_keys = {k for k in distances.keys() if k.islower()}
    all_paths: list[tuple[int, set[str], str]] = [(0, set(), "@")]
    distances_to_states: defaultdict[tuple[tuple[str, ...], str], int] = defaultdict(lambda: 10**12)

    while all_paths:
        distance, keys, current = heapq.heappop(all_paths)
        if not all_keys - keys:
            print(distance)
            return
        for possible_next_step, distance_to_next_step in distances[current].items():
            if possible_next_step.isupper():
                if possible_next_step.lower() not in keys:
                    continue
                new_keys = keys
            else:
                new_keys = keys.copy()
                new_keys.add(possible_next_step)
            state_tuple = (tuple(sorted(keys)), possible_next_step)
            if distances_to_states[state_tuple] <= distance + distance_to_next_step:
                continue
            distances_to_states[state_tuple] = distance + distance_to_next_step
            heapq.heappush(all_paths, (distance + distance_to_next_step, new_keys, possible_next_step))


def problem_2() -> None:
    width, height = len(lines[0]), len(lines)
    vertical_midpoint, horizontal_midpoint = height // 2, width // 2
    top_line = lines[vertical_midpoint - 1]
    middle_line = lines[vertical_midpoint]
    bottom_line = lines[vertical_midpoint + 1]
    lines[vertical_midpoint - 1] = top_line[: horizontal_midpoint - 1] + "@#@" + top_line[horizontal_midpoint + 2 :]
    lines[vertical_midpoint] = middle_line[: horizontal_midpoint - 1] + "###" + middle_line[horizontal_midpoint + 2 :]
    lines[vertical_midpoint + 1] = (
        bottom_line[: horizontal_midpoint - 1] + "@#@" + bottom_line[horizontal_midpoint + 2 :]
    )
    top_left_lines = [line[: horizontal_midpoint + 1] for line in lines[: vertical_midpoint + 1]]
    top_right_lines = [line[horizontal_midpoint:] for line in lines[: vertical_midpoint + 1]]
    bottom_left_lines = [line[: horizontal_midpoint + 1] for line in lines[vertical_midpoint:]]
    bottom_right_lines = [line[horizontal_midpoint:] for line in lines[vertical_midpoint:]]

    top_left_distances = get_distances(top_left_lines)
    top_right_distances = get_distances(top_right_lines)
    bottom_left_distances = get_distances(bottom_left_lines)
    bottom_right_distances = get_distances(bottom_right_lines)

    all_keys = {k for k in top_left_distances.keys() if k.islower()}
    all_keys.update({k for k in top_right_distances.keys() if k.islower()})
    all_keys.update({k for k in bottom_left_distances.keys() if k.islower()})
    all_keys.update({k for k in bottom_right_distances.keys() if k.islower()})

    all_paths: list[tuple[int, set[str], list[str]]] = [(0, set(), ["@", "@", "@", "@"])]
    distances_to_states: defaultdict[tuple[tuple[str, ...], tuple[str, ...]], int] = defaultdict(lambda: 10**12)

    while all_paths:
        distance, keys, all_current = heapq.heappop(all_paths)
        if not all_keys - keys:
            print(distance)
            return
        for i, quadrant_to_move in enumerate(
            (top_left_distances, top_right_distances, bottom_left_distances, bottom_right_distances)
        ):
            for possible_next_step, distance_to_next_step in quadrant_to_move[all_current[i]].items():
                if possible_next_step.isupper():
                    if possible_next_step.lower() not in keys:
                        continue
                    new_keys = keys
                else:
                    new_keys = keys.copy()
                    new_keys.add(possible_next_step)
                next_all_current = all_current[:i] + [possible_next_step] + all_current[i + 1 :]
                state_tuple = (tuple(sorted(keys)), tuple(next_all_current))
                if distances_to_states[state_tuple] <= distance + distance_to_next_step:
                    continue
                distances_to_states[state_tuple] = distance + distance_to_next_step
                heapq.heappush(all_paths, (distance + distance_to_next_step, new_keys, next_all_current))
