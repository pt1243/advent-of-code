with open("./2016/resources/1.txt") as f:
    steps = f.read().strip().split(", ")


def part_1() -> None:
    x, y = 0, 0
    directions = {0: (0, 1), 1: (1, 0), 2: (0, -1), 3: (-1, 0)}
    direction = 0

    for step in steps:
        turn = step[0]
        distance = int(step[1:])
        direction = (direction + (1 if turn == "R" else -1)) % 4
        dx, dy = directions[direction]
        x += dx * distance
        y += dy * distance
    print(abs(x) + abs(y))


def part_2() -> None:
    x, y = 0, 0
    directions = {0: (0, 1), 1: (1, 0), 2: (0, -1), 3: (-1, 0)}
    direction = 0
    seen: set[tuple[int, int]] = set()

    for step in steps:
        turn = step[0]
        distance = int(step[1:])
        direction = (direction + (1 if turn == "R" else -1)) % 4
        dx, dy = directions[direction]
        for _ in range(distance):
            x += dx
            y += dy
            if (x, y) in seen:
                print(abs(x) + abs(y))
                return
            seen.add((x, y))
