from itertools import pairwise, permutations


with open("./2015/resources/9.txt") as f:
    all_distances = [line.strip() for line in f]


def problem_1() -> None:
    destinations: set[str] = set()
    distances: dict[tuple[str, str], int] = {}
    for entry in all_distances:
        locations, _, dist = entry.partition(" = ")
        from_place, _, to_place = locations.partition(" to ")
        destinations.add(from_place)
        destinations.add(to_place)
        distances[(from_place, to_place)] = int(dist)

    shortest_distance: int | None = None
    for route in permutations(destinations):
        route_total = 0
        for start, end in pairwise(route):
            try:
                route_total += distances[(start, end)]
            except KeyError:
                route_total += distances[(end, start)]
        if shortest_distance is None or route_total < shortest_distance:
            shortest_distance = route_total

    print(shortest_distance)


def problem_2() -> None:
    destinations: set[str] = set()
    distances: dict[tuple[str, str], int] = {}
    for entry in all_distances:
        locations, _, dist = entry.partition(" = ")
        from_place, _, to_place = locations.partition(" to ")
        destinations.add(from_place)
        destinations.add(to_place)
        distances[(from_place, to_place)] = int(dist)

    longest_distance: int | None = None
    for route in permutations(destinations):
        route_total = 0
        for start, end in pairwise(route):
            try:
                route_total += distances[(start, end)]
            except KeyError:
                route_total += distances[(end, start)]
        if longest_distance is None or route_total > longest_distance:
            longest_distance = route_total

    print(longest_distance)
