from collections import defaultdict
from dataclasses import dataclass
from itertools import count
import heapq
from operator import itemgetter
from typing import Literal


with open("./2018/resources/15.txt") as f:
    lines = f.read().splitlines()


@dataclass
class Unit:
    unit_type: Literal["goblin", "elf"]
    attack_power: int = 3
    hp: int = 200
    already_took_turn: bool = False


def simulate_game(text_input: list[str], elf_attack_power: int = 3) -> tuple[int, bool]:
    offsets = ((-1, 0), (0, -1), (0, 1), (1, 0))
    board: list[list[bool | Unit]] = []
    all_units: list[Unit] = []
    num_elves = 0
    for line in text_input:
        board_row: list[bool | Unit] = []
        for char in line:
            if char == "G":
                unit = Unit("goblin")
                board_row.append(unit)
                all_units.append(unit)
            elif char == "E":
                unit = Unit("elf", elf_attack_power)
                board_row.append(unit)
                all_units.append(unit)
                num_elves += 1
            else:
                board_row.append(True if char == "." else False)
        board.append(board_row)

    def a_star(
        starting_row: int, starting_col: int, target: tuple[int, int]
    ) -> tuple[int | None, list[tuple[int, int]]]:
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
        new_row, new_col = first_step
        if min_dist > 1:
            first_step_offset = (first_step[0] - row, first_step[1] - col)
            idx = offsets.index(first_step_offset)
            if idx > 2:  # check going right first
                if board[row][col + 1] is True:
                    new_dist, _ = a_star(row, col + 1, move_to)
                    if new_dist == min_dist - 1:
                        new_row, new_col = row, col + 1
            if idx > 1:  # check going left first
                if board[row][col - 1] is True:
                    new_dist, _ = a_star(row, col - 1, move_to)
                    if new_dist == min_dist - 1:
                        new_row, new_col = row, col - 1
            if idx > 0:  # check going up first
                if board[row - 1][col] is True:
                    new_dist, _ = a_star(row - 1, col, move_to)
                    if new_dist == min_dist - 1:
                        new_row, new_col = row - 1, col

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
        selected_target.hp -= unit.attack_power
        if selected_target.hp <= 0:
            board[target_row][target_col] = True
            all_units.remove(selected_target)
        return

    for round_num in count(1):
        # mark all units as not moved
        for unit in all_units:
            unit.already_took_turn = False
        for row_idx, board_row in enumerate(board):
            for col_idx, item in enumerate(board_row):
                if isinstance(item, Unit) and not item.already_took_turn:
                    if all(unit.unit_type == "elf" for unit in all_units) or all(
                        unit.unit_type == "goblin" for unit in all_units
                    ):
                        return (round_num - 1) * sum(unit.hp for unit in all_units), len(
                            all_units
                        ) == num_elves and all_units[0].unit_type == "elf"
                    new_row, new_col = move(item, row_idx, col_idx)
                    attack(item, new_row, new_col)
    assert False  # so that mypy can be sure that this is unreachable


def problem_1() -> None:
    outcome, _ = simulate_game(lines)
    print(outcome)


def problem_2() -> None:
    for elf_attack_power in count(4):
        outcome, no_elves_dead = simulate_game(lines, elf_attack_power)
        if no_elves_dead:
            print(outcome)
            return
