with open("./2025/resources/1.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    current_dial_number = 50
    on_zero = 0
    for line in lines:
        direction = -1 if line[0] == "L" else 1
        distance = int(line[1:])
        current_dial_number += direction * distance
        current_dial_number %= 100
        if current_dial_number == 0:
            on_zero += 1
    print(on_zero)


def problem_2() -> None:
    current_dial_number = 50
    zeros = 0
    for line in lines:
        direction = -1 if line[0] == "L" else 1
        distance = int(line[1:])
        full_turns, rest = divmod(distance, 100)
        zeros += full_turns
        turns, new_dial_number = divmod(current_dial_number + rest * direction, 100)
        if new_dial_number == 0:
            zeros += 1
        elif current_dial_number != 0:
            zeros += abs(turns)
        current_dial_number = new_dial_number
    print(zeros)
