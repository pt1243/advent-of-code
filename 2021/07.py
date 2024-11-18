with open("./2021/resources/7.txt") as f:
    positions = sorted([int(x) for x in f.read().strip().split(",")])


def problem_1() -> None:
    current_position = positions[0]
    current_fuel = sum(abs(pos - current_position) for pos in positions)
    while True:
        new_position = current_position + 1
        new_fuel = sum(abs(pos - new_position) for pos in positions)
        if new_fuel > current_fuel:
            print(current_fuel)
            break
        current_position = new_position
        current_fuel = new_fuel


def problem_2() -> None:
    current_position = positions[0]
    current_fuel = sum((abs(pos - current_position) * (abs(pos - current_position) + 1)) // 2 for pos in positions)
    while True:
        new_position = current_position + 1
        new_fuel = sum((abs(pos - new_position) * (abs(pos - new_position) + 1)) // 2 for pos in positions)
        if new_fuel > current_fuel:
            print(current_fuel)
            break
        current_position = new_position
        current_fuel = new_fuel
