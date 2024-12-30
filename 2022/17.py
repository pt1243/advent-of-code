from itertools import count, cycle
from typing import NamedTuple


with open("./2022/resources/17.txt") as f:
    text = f.read().strip()


class Rock(NamedTuple):
    width: int
    positions: list[tuple[int, int]]


def problem_1() -> None:
    all_rocks = cycle(
        (
            Rock(4, [(0, 0), (0, 1), (0, 2), (0, 3)]),
            Rock(3, [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]),
            Rock(3, [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]),
            Rock(1, [(0, 0), (1, 0), (2, 0), (3, 0)]),
            Rock(2, [(0, 0), (0, 1), (1, 0), (1, 1)]),
        )
    )
    gas_jets = cycle(text)
    at_rest = {(0, i) for i in range(7)}
    highest_point = 0

    for _ in range(2022):
        rock_row = highest_point + 4
        rock_col = 2
        rock = next(all_rocks)
        while True:
            direction = next(gas_jets)
            if (
                direction == "<"
                and rock_col > 0
                and all((rock_row + drow, rock_col + dcol - 1) not in at_rest for (drow, dcol) in rock.positions)
            ):
                rock_col -= 1
            elif (
                direction == ">"
                and rock_col < 7 - rock.width
                and all((rock_row + drow, rock_col + dcol + 1) not in at_rest for (drow, dcol) in rock.positions)
            ):
                rock_col += 1
            if all((rock_row + drow - 1, rock_col + dcol) not in at_rest for (drow, dcol) in rock.positions):
                rock_row -= 1
            else:
                rock_positions = {(rock_row + drow, rock_col + dcol) for (drow, dcol) in rock.positions}
                at_rest |= rock_positions
                highest_point = max(highest_point, max(pos[0] for pos in rock_positions))
                break
    print(highest_point)


def problem_2() -> None:
    all_rocks = cycle(
        enumerate(
            (
                Rock(4, [(0, 0), (0, 1), (0, 2), (0, 3)]),
                Rock(3, [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]),
                Rock(3, [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]),
                Rock(1, [(0, 0), (1, 0), (2, 0), (3, 0)]),
                Rock(2, [(0, 0), (0, 1), (1, 0), (1, 1)]),
            )
        )
    )
    gas_jets = cycle(enumerate(text))
    at_rest = {(0, i) for i in range(7)}
    highest_point = 0
    seen: dict[tuple[tuple[int, ...], int, int], tuple[int, int]] = {}

    cycle_length = 0
    cycle_height_difference = 0
    target_modulus = 0
    target = 1000000000000 - 1  # zero-indexing
    for i in count():
        rock_row = highest_point + 4
        rock_col = 2
        rock_index, rock = next(all_rocks)
        while True:
            char_index, direction = next(gas_jets)
            if (
                direction == "<"
                and rock_col > 0
                and all((rock_row + drow, rock_col + dcol - 1) not in at_rest for (drow, dcol) in rock.positions)
            ):
                rock_col -= 1
            elif (
                direction == ">"
                and rock_col < 7 - rock.width
                and all((rock_row + drow, rock_col + dcol + 1) not in at_rest for (drow, dcol) in rock.positions)
            ):
                rock_col += 1
            if all((rock_row + drow - 1, rock_col + dcol) not in at_rest for (drow, dcol) in rock.positions):
                rock_row -= 1
            else:
                rock_positions = {(rock_row + drow, rock_col + dcol) for (drow, dcol) in rock.positions}
                at_rest |= rock_positions
                highest_point = max(highest_point, max(pos[0] for pos in rock_positions))
                heights_to_top = tuple(
                    [highest_point - max(pos[0] for pos in at_rest if pos[1] == col) for col in range(7)]
                )
                key = (heights_to_top, char_index, rock_index)
                if key in seen:
                    if not cycle_length:  # first reoccurence gives the cycle length and height difference
                        cycle_height_difference = highest_point - seen[key][0]
                        cycle_length = i - seen[key][1]
                        target_modulus = target % cycle_length
                    elif i % cycle_length == target_modulus:
                        print((target - i) // cycle_length * cycle_height_difference + highest_point)
                        return
                seen[key] = (highest_point, i)
                break
