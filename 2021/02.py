with open("./2021/resources/2.txt") as f:
    lines = f.readlines()


def problem_1() -> None:
    horizontal = 0
    depth = 0
    for line in lines:
        direction, distance_str = line.split()
        distance = int(distance_str)
        if direction == "down":
            depth += distance
        elif direction == "up":
            depth -= distance
        else:
            horizontal += distance
    print(horizontal * depth)


def problem_2() -> None:
    horizontal = 0
    depth = 0
    aim = 0
    for line in lines:
        direction, value_str = line.split()
        value = int(value_str)
        if direction == "down":
            aim += value
        elif direction == "up":
            aim -= value
        else:
            horizontal += value
            depth += aim * value
    print(horizontal * depth)
