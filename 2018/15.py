from collections import defaultdict, deque
from dataclasses import dataclass
from itertools import count
import heapq
from operator import itemgetter
from typing import Literal


with open("./2018/resources/15.txt") as f:
    lines = [line.strip() for line in f]

test_lines_1 = """
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######
""".strip().split("\n")

test_lines_2 = """
#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######
""".strip().split("\n")

test_lines_3 = """
#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######
""".strip().split("\n")

test_lines_4 = """
#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######
""".strip().split("\n")

test_lines_5 = """
#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######
""".strip().split("\n")

test_lines_6 = """
#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########
""".strip().split("\n")


@dataclass
class Unit:
    unit_type: Literal["goblin", "elf"]
    attack_power: int = 3
    hp: int = 200
    already_took_turn: bool = False


def simulate_game(text_input: list[str]) -> int:
    offsets = ((-1, 0), (0, -1), (0, 1), (1, 0))
    board: list[list[bool | Unit]] = []
    all_units: list[Unit] = []
    for line in text_input:
        board_row: list[bool | Unit] = []
        for char in line:
            if char == "G":
                unit = Unit("goblin")
                board_row.append(unit)
                all_units.append(unit)
            elif char == "E":
                unit = Unit("elf")
                board_row.append(unit)
                all_units.append(unit)
            else:
                board_row.append(True if char == "." else False)
        board.append(board_row)

    def a_star(starting_row: int, starting_col: int, target: tuple[int, int]) -> tuple[int | None, list[tuple[int, int]]]:
        open_set = [(0, starting_row, starting_col)]
        came_from: dict[tuple[int, int], tuple[int, int]] = {}
        g_score = defaultdict(lambda: 10**12)
        g_score[(starting_row, starting_col)] = 0
        f_score = defaultdict(lambda: 10**12)
        f_score[(starting_row, starting_col)] = abs(starting_row - target[0]) + abs(starting_col - target[1])
        while open_set:
            _, row, col = heapq.heappop(open_set)
            current = (row, col)
            if current == target:
                path = [current]
                while current in came_from.keys():
                    current = came_from[current]
                    path.append(current)
                return g_score[target], path[::-1]
            neighbours = [(row + offset[0], col + offset[1]) for offset in offsets]
            for new_row, new_col in neighbours:
                neighbour = (new_row, new_col)
                item = board[new_row][new_col]
                if item is not True:
                    continue
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score[neighbour]:
                    came_from[neighbour] = current
                    g_score[neighbour] = tentative_g_score
                    f_score_neighbour = tentative_g_score + abs(new_row - target[0]) + abs(new_col - target[1])
                    f_score[neighbour] = f_score_neighbour
                    heapq.heappush(open_set, (f_score_neighbour, new_row, new_col))
        return None, []

    def find_min_paths(starting_row: int, starting_col: int, target: tuple[int, int], min_dist: int) -> list[list[tuple[int, int]]]:
        all_shortest_paths: list[list[tuple[int, int]]] = []
        queue = deque([[(starting_row, starting_col)]])
        while queue:
            current_path = queue.popleft()
            # if the next shortest path is longer than the min dist, we have checked all shortest paths
            current_path_length = len(current_path)
            if current_path_length > min_dist + 1:
                break
            last_pos_row, last_pos_col = current_path[-1]
            if (last_pos_row, last_pos_col) == target:
                all_shortest_paths.append(current_path)
            for offset in offsets:
                if board[last_pos_row + offset[0]][last_pos_col + offset[1]] is True:
                    queue.append(current_path + [(last_pos_row + offset[0], last_pos_col + offset[1])])
        return all_shortest_paths
        


    def move(unit: Unit, row: int, col: int) -> tuple[int, int]:
        # check if we are already in range
        for offset in offsets:
            item = board[row + offset[0]][col + offset[1]]
            if isinstance(item, Unit) and item.unit_type != unit.unit_type:
                return row, col
        target_positions: set[tuple[int, int]] = set()
        for i, board_row in enumerate(board):
            for j, position in enumerate(board_row):
                if isinstance(position, Unit) and position.unit_type != unit.unit_type:
                    for offset in offsets:
                        if board[i + offset[0]][j + offset[1]] is True:
                            target_positions.add((i + offset[0], j + offset[1]))
        if not target_positions:  # no in-range positions
            return row, col

        # find nearest positions
        target_position_distances: dict[tuple[int, int], int] = {}
        for target in target_positions:
            dist, _ = a_star(row, col, target)
            if dist is None:
                continue
            target_position_distances[target] = dist
        
        # select position to move towards
        if not target_position_distances:  # no in-range positions are accessible
            return row, col
        min_dist = min(target_position_distances.values())
        move_to = min([t for t, dist in target_position_distances.items() if dist == min_dist])
        
        _, path = a_star(row, col, move_to)
        first_step = path[1]
        # FIXME: need to consider all other directions lower in reading order
        if first_step[0] - row == -1:  # first move up; already in reading order, continue
            pass
        elif first_step[0] == row:  # first move left or right; check moving up first
            if board[row - 1][col] is True:
                dist, new_path = a_star(row - 1, col, move_to)
                if dist == min_dist - 1:
                    first_step = new_path[1]
        else:  # first move down; check moving left first
            if board[row][col - 1] is True:
                dist, new_path = a_star(row, col - 1, move_to)
                if dist == min_dist - 1:
                    first_step = new_path[1]

        # get the minimum distance paths
        all_shortest_paths = find_min_paths(row, col, move_to, min_dist)
        new_row, new_col = min(all_shortest_paths)[1]
        if (new_row, new_col) != first_step:
            print(f"{row = }, {col = }, {move_to = }, {new_row = }, {new_col = }, {first_step = }")
            print(new_path)
        # next_steps: list[tuple[int, int]] = []
        # for offset in offsets:
        #     if board[row + offset[0]][col + offset[1]] is True:
        #         dist, path = a_star(row + offset[0], col + offset[1], move_to)
        #         if dist == min_dist - 1:
        #             if len(path) == 1:
        #                 breakpoint()
        #                 next_steps.append(path[0])
        #             else:
        #                 next_steps.append(path[1])
        # new_row, new_col = min(next_steps)


        board[row][col] = True
        board[new_row][new_col] = unit
        unit.already_took_turn = True
        return new_row, new_col
    
    def attack(unit: Unit, row: int, col: int) -> None:
        possible_targets_and_positions: list[tuple[Unit, int, int]] = []
        for offset in offsets:
            item = board[row + offset[0]][col + offset[1]]
            if isinstance(item, Unit) and item.unit_type != unit.unit_type:
                possible_targets_and_positions.append((item, row + offset[0], col + offset[1]))
        if not possible_targets_and_positions:
            return
        min_hp = min([t[0].hp for t in possible_targets_and_positions])
        min_hp_targets = [t for t in possible_targets_and_positions if t[0].hp == min_hp]
        selected_target_and_position = min(min_hp_targets, key=itemgetter(1, 2))
        selected_target = selected_target_and_position[0]
        target_row, target_col = selected_target_and_position[1], selected_target_and_position[2]
        # print(f"{unit} at {row = }, {col = } selected {selected_target} at {target_row = }, {target_col = };", end="")
        selected_target.hp -= unit.attack_power
        # print(f" target hp is now {selected_target.hp}")
        if selected_target.hp <= 0:
            board[target_row][target_col] = True
            all_units.remove(selected_target)
        return

    finished = False
    for round_num in count(1):
        # print(f"Round {round_num}")
        # mark all units as not moved
        for unit in all_units:
            unit.already_took_turn = False
        # movement
        for row_idx, board_row in enumerate(board):
            for col_idx, item in enumerate(board_row):
                if isinstance(item, Unit) and not item.already_took_turn:
                    if all(unit.unit_type == "elf" for unit in all_units) or all(unit.unit_type == "goblin" for unit in all_units):
                        # print(f"ending on round {round_num - 1} with {item} at {row_idx = }, {col_idx = }")
                        finished = True
                        break
                    new_row, new_col = move(item, row_idx, col_idx)
                    attack(item, new_row, new_col)
            if finished:
                break
        if finished:
            break
        # print(f"\nAfter {round_num} rounds:")
        # for r in board:
        #     s = ""
        #     extra_data = ""
        #     for c in r:
        #         if isinstance(c, Unit):
        #             s += "G" if c.unit_type == "goblin" else "E"
        #             extra_data += "G" if c.unit_type == "goblin" else "E"
        #             extra_data += f"({c.hp})  "
        #         else:
        #             s += "." if c else "#"
        #     print(f"{s}    {extra_data}")
    
    print("\n")
    for r in board:
        s = ""
        extra_data = ""
        for c in r:
            if isinstance(c, Unit):
                s += "G" if c.unit_type == "goblin" else "E"
                extra_data += "G" if c.unit_type == "goblin" else "E"
                extra_data += f"({c.hp})  "
            else:
                s += "." if c else "#"
        print(f"{s}    {extra_data}")
    
    round_num -= 1
    print(f"\nCombat ends after {round_num} full rounds")
    total_hp = sum(unit.hp for unit in all_units)
    print(f"{'Goblins' if all_units[0].unit_type == 'goblin' else 'Elves'} win with {total_hp} total hit points left")
    print(f"Outcome: {round_num * total_hp}")
    return round_num * sum(unit.hp for unit in all_units)
    # top_goblin = board[1][1]
    # move(top_goblin, 1, 1)
    # elf = board[4][4]
    # move(elf, 4, 4)


def problem_1() -> None:
    simulate_game(test_lines_1)
    # simulate_game(test_lines_2)
    # simulate_game(test_lines_3)
    # simulate_game(test_lines_4)
    # simulate_game(test_lines_5)
    # simulate_game(test_lines_6)
    # simulate_game(lines)