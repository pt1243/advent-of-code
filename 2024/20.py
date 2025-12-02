from collections import defaultdict

with open("./2024/resources/20.txt") as f:
    lines = f.read().splitlines()


def get_distances() -> dict[tuple[int, int], int]:
    distances: dict[tuple[int, int], int] = {}
    end_row = next(i for i, line in enumerate(lines) if "E" in line)
    end_col = lines[end_row].index("E")
    directions = ((-1, 0), (0, 1), (1, 0), (0, -1))

    open_set = [(0, end_row, end_col)]
    while open_set:
        dist, row, col = open_set.pop()
        distances[row, col] = dist
        for drow, dcol in directions:
            new_row = row + drow
            new_col = col + dcol
            if (new_row, new_col) not in distances and lines[new_row][new_col] != "#":
                open_set.append((dist + 1, new_row, new_col))
    return distances


def count_cheats(distances: dict[tuple[int, int], int], cheat_distance: int) -> int:
    counts: defaultdict[int, int] = defaultdict(int)
    for cheat_start in distances:
        for drow in range(-cheat_distance, cheat_distance + 1):
            for dcol in range(-cheat_distance + abs(drow), cheat_distance - abs(drow) + 1):
                cheat_end = (cheat_start[0] + drow, cheat_start[1] + dcol)
                if cheat_end in distances:
                    cheat_savings = distances[cheat_start] - distances[cheat_end] - abs(drow) - abs(dcol)
                    if cheat_savings > 0:
                        counts[cheat_savings] += 1
    return sum(count for distance, count in counts.items() if distance >= 100)


def problem_1() -> None:
    distances = get_distances()
    print(count_cheats(distances, 2))


def problem_2() -> None:
    distances = get_distances()
    print(count_cheats(distances, 20))
