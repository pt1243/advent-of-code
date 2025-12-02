from math import cos, radians, sin

with open("./2020/resources/12.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
    direction = 1
    x, y = 0, 0
    for line in lines:
        action = line[0]
        value = int(line[1:])
        if action == "N":
            y += value
        elif action == "S":
            y -= value
        elif action == "E":
            x += value
        elif action == "W":
            x -= value
        elif action == "L":
            turns = value // 90
            direction -= turns
            direction %= 4
        elif action == "R":
            turns = value // 90
            direction += turns
            direction %= 4
        else:
            dx, dy = directions[direction]
            x += dx * value
            y += dy * value
    print(abs(x) + abs(y))


def problem_2() -> None:
    x, y = 0, 0
    waypoint_x, waypoint_y = 10, 1
    for line in lines:
        action = line[0]
        value = int(line[1:])
        if action == "N":
            waypoint_y += value
        elif action == "S":
            waypoint_y -= value
        elif action == "E":
            waypoint_x += value
        elif action == "W":
            waypoint_x -= value
        elif action == "F":
            x += value * waypoint_x
            y += value * waypoint_y
        else:
            theta = radians(value * (1 if action == "L" else -1))
            new_waypoint_x = round(waypoint_x * cos(theta) - waypoint_y * sin(theta))
            new_waypoint_y = round(waypoint_x * sin(theta) + waypoint_y * cos(theta))
            waypoint_x, waypoint_y = new_waypoint_x, new_waypoint_y
    print(abs(x) + abs(y))
