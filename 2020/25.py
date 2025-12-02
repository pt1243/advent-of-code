with open("./2020/resources/25.txt") as f:
    lines = f.read().splitlines()


def part_1() -> None:
    card_target = int(lines[0])
    door_target = int(lines[1])

    card_loop_size = 0
    value = 1
    while value != card_target:
        value *= 7
        value %= 20201227
        card_loop_size += 1

    encryption_key = 1
    for _ in range(card_loop_size):
        encryption_key *= door_target
        encryption_key %= 20201227

    print(encryption_key)
