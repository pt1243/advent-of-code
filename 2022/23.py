from collections import defaultdict, deque
from itertools import count


with open("./2022/resources/23.txt") as f:
    lines = f.read().splitlines()


def run_moves(lines: list[str], part_2: bool = False) -> int:
    positions: set[tuple[int, int]] = set()
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == "#":
                positions.add((row, col))
    position_order = deque(((-1, 0), (1, 0), (0, -1), (0, 1)))

    for i in count(1):
        proposed_positions: defaultdict[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)
        for row, col in positions:
            num_neighbours = (
                sum((row + drow, col + dcol) in positions for drow in range(-1, 2) for dcol in range(-1, 2)) - 1
            )
            if num_neighbours == 0:
                continue
            for drow, dcol in position_order:
                positions_to_check = {(row + drow, col + dcol)}
                if dcol == 0:
                    positions_to_check |= {(row + drow, col - 1), (row + drow, col + 1)}
                else:
                    positions_to_check |= {(row - 1, col + dcol), (row + 1, col + dcol)}
                if not positions_to_check & positions:
                    proposed_positions[row + drow, col + dcol].add((row, col))
                    break

        any_moved = False
        new_positions: set[tuple[int, int]] = set()
        for proposed_new_position, elves_wanting_to_move in proposed_positions.items():
            if len(elves_wanting_to_move) == 1:
                new_positions.add(proposed_new_position)
                positions.remove(elves_wanting_to_move.pop())
                any_moved = True
            else:
                new_positions.update(elves_wanting_to_move)
                positions -= elves_wanting_to_move
        positions |= new_positions
        position_order.rotate(-1)
        if not part_2 and i == 10:
            height = max(pos[0] for pos in positions) - min(pos[0] for pos in positions) + 1
            width = max(pos[1] for pos in positions) - min(pos[1] for pos in positions) + 1
            return height * width - len(positions)
        if part_2 and not any_moved:
            return i
    assert False


def problem_1() -> None:
    print(run_moves(lines))


def problem_2() -> None:
    print(run_moves(lines, part_2=True))
