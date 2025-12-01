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
    on_zero = 0
    for line in lines:
        direction = -1 if line[0] == "L" else 1
        distance = int(line[1:])
        for _ in range(distance):
            current_dial_number += direction
            current_dial_number %= 100
            if current_dial_number == 0:
                on_zero += 1
    print(on_zero)
