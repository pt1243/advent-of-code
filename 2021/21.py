from functools import cache
from itertools import cycle

with open("./2021/resources/21.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    die = cycle(range(1, 101))
    die_rolls = 0
    player_1_score, player_2_score = 0, 0

    player_1_position = int(lines[0].split()[-1]) - 1
    player_2_position = int(lines[1].split()[-1]) - 1

    while True:
        player_1_position += next(die) + next(die) + next(die)
        die_rolls += 3
        player_1_position %= 10
        player_1_score += player_1_position + 1

        if player_1_score >= 1000:
            print(player_2_score * die_rolls)
            break

        player_2_position += next(die) + next(die) + next(die)
        die_rolls += 3
        player_2_position %= 10
        player_2_score += player_2_position + 1

        if player_2_score >= 1000:
            print(player_1_score * die_rolls)
            break


def problem_2() -> None:
    frequencies = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}

    @cache
    def count_player_1_wins(
        player_1_pos: int, player_2_pos: int, player_1_score: int, player_2_score: int, player_1_turn: bool
    ) -> int:
        if player_1_score >= 21:
            return 1
        if player_2_score >= 21:
            return 0

        if player_1_turn:
            return sum(
                frequency
                * count_player_1_wins(
                    (player_1_pos + roll_total) % 10,
                    player_2_pos,
                    player_1_score + ((player_1_pos + roll_total) % 10) + 1,
                    player_2_score,
                    False,
                )
                for roll_total, frequency in frequencies.items()
            )
        else:
            return sum(
                frequency
                * count_player_1_wins(
                    player_1_pos,
                    (player_2_pos + roll_total) % 10,
                    player_1_score,
                    player_2_score + ((player_2_pos + roll_total) % 10) + 1,
                    True,
                )
                for roll_total, frequency in frequencies.items()
            )

    player_1_position = int(lines[0].split()[-1]) - 1
    player_2_position = int(lines[1].split()[-1]) - 1

    print(
        max(
            count_player_1_wins(player_1_position, player_2_position, 0, 0, True),
            count_player_1_wins(player_2_position, player_1_position, 0, 0, False),
        )
    )
