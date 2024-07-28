from collections import defaultdict


with open("./2023/resources/2.txt") as f:
    lines = [line.strip() for line in f]


def problem_1() -> None:
    limits = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }
    sum_game_ids = 0
    for game in lines:
        game_info, observations = game.split(": ")
        game_id = int(game_info.split()[1])
        possible = True
        for observation in observations.split("; "):
            for dice_observed in observation.split(", "):
                split = dice_observed.split()
                num, colour = int(split[0]), split[1]
                for limited_colour, limit in limits.items():
                    if colour == limited_colour and num > limit:
                        possible = False
                        break
        if possible:
            sum_game_ids += game_id
    print(sum_game_ids)


def problem_2() -> None:
    total_power = 0
    for game in lines:
        observations = game.split(": ")[1]
        min_dice: defaultdict[str, int] = defaultdict(int)
        for observation in observations.split("; "):
            for dice_observed in observation.split(", "):
                split = dice_observed.split()
                num, colour = int(split[0]), split[1]
                min_dice[colour] = max(min_dice[colour], num)
        power = min_dice["red"] * min_dice["green"] * min_dice["blue"]
        total_power += power
    print(total_power)
