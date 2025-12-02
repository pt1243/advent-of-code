from typing import NamedTuple

with open("./2016/resources/22.txt") as f:
    lines = f.read().splitlines()[2:]


class Node(NamedTuple):
    x: int
    y: int
    size: int
    used: int
    avail: int


def problem_1() -> None:
    all_nodes: list[Node] = []
    for line in lines:
        split = line.split()
        all_nodes.append(
            Node(
                int(split[0][split[0].index("-") + 2 : split[0].rindex("-")]),
                int(split[0][split[0].rindex("-") + 2 :]),
                int(split[1][:-1]),
                int(split[2][:-1]),
                int(split[3][:-1]),
            )
        )
    found_viable_pairs = 0
    for a in all_nodes:
        for b in all_nodes:
            if a.used == 0:
                continue
            if a == b:
                continue
            if a.used <= b.avail:
                found_viable_pairs += 1
    print(found_viable_pairs)


def problem_2() -> None:
    all_nodes: list[Node] = []
    for line in lines:
        split = line.split()
        all_nodes.append(
            Node(
                int(split[0][split[0].index("-") + 2 : split[0].rindex("-")]),
                int(split[0][split[0].rindex("-") + 2 :]),
                int(split[1][:-1]),
                int(split[2][:-1]),
                int(split[3][:-1]),
            )
        )
    max_x = max((node.x for node in all_nodes))

    large_size_threshold = 400
    large_node_positions = [(node.x, node.y) for node in all_nodes if node.size > large_size_threshold]
    empty_position = [(node.x, node.y) for node in all_nodes if node.used == 0][0]

    large_positions_y = large_node_positions[0][1]
    large_positions_start_x = sorted(large_node_positions)[0][0]

    steps_to_move_next_to_g = max_x - empty_position[0] + empty_position[1]
    if empty_position[1] > large_positions_y and large_positions_start_x <= empty_position[0]:
        steps_to_move_next_to_g += 2 * (empty_position[0] - large_positions_start_x + 1)
    g_starting_dist = max_x - 1
    print(steps_to_move_next_to_g + 5 * g_starting_dist)
