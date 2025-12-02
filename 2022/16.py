from collections import defaultdict
from collections.abc import Mapping, Sequence
from itertools import combinations, pairwise

from more_itertools import set_partitions

with open("./2022/resources/16.txt") as f:
    lines = f.read().splitlines()


def get_valve_connections(lines: list[str]) -> tuple[dict[str, int], defaultdict[str, dict[str, int]], dict[str, int]]:
    connections: dict[str, list[str]] = {}
    valve_flow_rates: dict[str, int] = {}
    for line in lines:
        split = line.split(maxsplit=9)
        valve_name = split[1]
        rate = int(split[4].split("=")[1].rstrip(";"))
        if rate:
            valve_flow_rates[valve_name] = rate
        connections[valve_name] = split[-1].split(", ")

    # Floyd-Warshall
    indices = {val: i for i, val in enumerate(connections)}
    num_edges = sum(len(c) for c in connections.values())
    dist = [[10**6 for _ in range(num_edges)] for _ in range(num_edges)]
    for u, ends in connections.items():
        dist[indices[u]][indices[u]] = 0
        for v in ends:
            dist[indices[u]][indices[v]] = 1
    for k in range(num_edges):
        for i in range(num_edges):
            for j in range(num_edges):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    distances_between_valves: defaultdict[str, dict[str, int]] = defaultdict(dict)
    for start, end in combinations(valve_flow_rates, 2):
        i, j = indices[start], indices[end]
        distances_between_valves[start][end] = dist[i][j]
        distances_between_valves[end][start] = dist[j][i]
    distances_from_AA = {end: dist[indices["AA"]][indices[end]] for end in valve_flow_rates}
    return valve_flow_rates, distances_between_valves, distances_from_AA


def calculate_pressure_released(
    path: Sequence[str],
    valve_flow_rates: Mapping[str, int],
    distances_between_valves: Mapping[str, Mapping[str, int]],
    distances_from_AA: Mapping[str, int],
    time_available: int,
) -> int:
    pressure_released = 0
    pressure_per_minute = 0
    minute = 1 + distances_from_AA[path[0]]
    for valve_1, valve_2 in pairwise(path):
        travel_time = 1 + distances_between_valves[valve_1][valve_2]
        minute += travel_time
        pressure_per_minute += valve_flow_rates[valve_1]
        pressure_released += travel_time * pressure_per_minute
    pressure_per_minute += valve_flow_rates[path[-1]]
    pressure_released += (time_available - minute) * pressure_per_minute
    return pressure_released


def get_max_pressure_released(
    valve_flow_rates: Mapping[str, int],
    distances_between_valves: Mapping[str, Mapping[str, int]],
    distances_from_AA: Mapping[str, int],
    allowed: set[str],
    time_available: int,
) -> int:
    open_set = [
        (1 + start_distance, [start_point], {start_point})
        for start_point, start_distance in distances_from_AA.items()
        if start_point in allowed
    ]
    max_pressure_released = 0
    while open_set:
        minute, path, seen = open_set.pop()
        max_pressure_released = max(
            max_pressure_released,
            calculate_pressure_released(
                path, valve_flow_rates, distances_between_valves, distances_from_AA, time_available
            ),
        )
        current = path[-1]
        for connection, distance in distances_between_valves[current].items():
            if connection in allowed and connection not in seen and minute + distance + 1 <= 30:
                open_set.append((minute + distance + 1, path + [connection], seen | {connection}))
    return max_pressure_released


def problem_1() -> None:
    valve_flow_rates, distances_between_valves, distances_from_AA = get_valve_connections(lines)
    print(
        get_max_pressure_released(
            valve_flow_rates, distances_between_valves, distances_from_AA, set(valve_flow_rates.keys()), 30
        )
    )


def problem_2() -> None:
    valve_flow_rates, distances_between_valves, distances_from_AA = get_valve_connections(lines)

    print(
        max(
            get_max_pressure_released(
                valve_flow_rates, distances_between_valves, distances_from_AA, set(visited_in_person), 26
            )
            + get_max_pressure_released(
                valve_flow_rates, distances_between_valves, distances_from_AA, set(visited_elephant), 26
            )
            for visited_in_person, visited_elephant in set_partitions(valve_flow_rates.keys(), 2)
        )
    )
