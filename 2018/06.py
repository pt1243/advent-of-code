from collections import defaultdict


with open("./2018/resources/6.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    coordinates = [(int(line.split(", ")[0]), int(line.split(", ")[1])) for line in lines]
    min_x = min((c[0] for c in coordinates))
    min_y = min((c[1] for c in coordinates))
    max_x = max((c[0] for c in coordinates))
    max_y = max((c[1] for c in coordinates))
    infinite_indices = {
        i for i, c in enumerate(coordinates) if c[0] == min_x or c[0] == max_x or c[1] == min_y or c[1] == max_y
    }
    num_closest_points: defaultdict[int, int] = defaultdict(int)
    for i in range(min_x, max_x + 1):
        for j in range(min_y, max_y + 1):
            distances = [abs(i - c[0]) + abs(j - c[1]) for c in coordinates]
            min_distance = min(distances)
            min_indices = [i for i, d in enumerate(distances) if d == min_distance]
            if len(min_indices) == 1:
                num_closest_points[min_indices[0]] += 1
    print(max([num_points for i, num_points in num_closest_points.items() if i not in infinite_indices]))


def problem_2() -> None:
    coordinates = [(int(line.split(", ")[0]), int(line.split(", ")[1])) for line in lines]
    min_x = min((c[0] for c in coordinates))
    min_y = min((c[1] for c in coordinates))
    max_x = max((c[0] for c in coordinates))
    max_y = max((c[1] for c in coordinates))
    total_distance_limit = 10_000
    average_distance = total_distance_limit // len(coordinates) + 1
    region_size = 0
    for i in range(min_x - average_distance, max_x + average_distance + 1):
        for j in range(min_y - average_distance, max_y + average_distance + 1):
            distances = [abs(i - c[0]) + abs(j - c[1]) for c in coordinates]
            if sum(distances) < total_distance_limit:
                region_size += 1
    print(region_size)
