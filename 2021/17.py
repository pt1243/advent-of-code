from math import ceil, floor, sqrt

with open("./2021/resources/17.txt") as f:
    text = f.read().strip()


def problem_1() -> None:
    *_, x_range, y_range = text.split()
    x_values = x_range[2:-1].split("..")
    y_values = y_range[2:].split("..")
    min_x = int(x_values[0])
    max_x = int(x_values[1])
    min_y = int(y_values[0])
    max_y = int(y_values[1])

    def hits_target(x_vel: int, y_vel: int) -> bool:
        x, y = 0, 0
        while x <= max_x and y >= min_y:
            x += x_vel
            y += y_vel
            x_vel -= 1 if x_vel > 0 else 0
            y_vel -= 1
            if min_x <= x <= max_x and min_y <= y <= max_y:
                return True
        return False

    min_x_vel = ceil(sqrt(2 * min_x)) - 1
    max_x_vel = floor(sqrt(2 * max_x)) + 1
    max_y_vel = 0
    for y_vel in range(200):  # somewhat arbitrary
        if any(hits_target(x_vel, y_vel) for x_vel in range(min_x_vel, max_x_vel + 1)):
            max_y_vel = y_vel

    height = (max_y_vel * (max_y_vel + 1)) // 2
    print(height)


def problem_2() -> None:
    *_, x_range, y_range = text.split()
    x_values = x_range[2:-1].split("..")
    y_values = y_range[2:].split("..")
    min_x = int(x_values[0])
    max_x = int(x_values[1])
    min_y = int(y_values[0])
    max_y = int(y_values[1])

    def hits_target(x_vel: int, y_vel: int) -> bool:
        x, y = 0, 0
        while x <= max_x and y >= min_y:
            x += x_vel
            y += y_vel
            x_vel -= 1 if x_vel > 0 else 0
            y_vel -= 1
            if min_x <= x <= max_x and min_y <= y <= max_y:
                return True
        return False

    print(sum(hits_target(x_vel, y_vel) for x_vel in range(0, max_x + 1) for y_vel in range(-200, 200)))
