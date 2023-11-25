from enum import Enum


with open('./2016/resources/1.txt') as f:
    steps = f.read().strip().split(", ")


class Direction(Enum):
    N = 0
    E = 1
    S = 2
    W = 3


def problem_1():
    x, y = 0, 0
    direction: Direction = Direction.N

    for step in steps:
        turn = step[0]
        distance = int(step[1:])
        
        direction = Direction((direction.value + (1 if turn == "R" else -1)) % 4)

        if direction is Direction.N:
            y += distance
        elif direction is Direction.E:
            x += distance
        elif direction is Direction.S:
            y -= distance
        else:
            x -= distance
    
    print(abs(x) + abs(y))


def problem_2():
    x, y = 0, 0
    direction: Direction = Direction.N
    seen: set[tuple[int, int]] = set()

    for step in steps:
        turn = step[0]
        distance = int(step[1:])
        
        direction = Direction((direction.value + (1 if turn == "R" else -1)) % 4)
        
        if direction is Direction.N:
            for _ in range(distance):
                y += 1
                if (x, y) in seen:
                    print(abs(x) + abs(y))
                    return
                seen.add((x, y))
        elif direction is Direction.E:
            for _ in range(distance):
                x += 1
                if (x, y) in seen:
                    print(abs(x) + abs(y))
                    return
                seen.add((x, y))
        elif direction is Direction.S:
            for _ in range(distance):
                y -= 1
                if (x, y) in seen:
                    print(abs(x) + abs(y))
                    return
                seen.add((x, y))
        else:
            for _ in range(distance):
                x -= 1
                if (x, y) in seen:
                    print(abs(x) + abs(y))
                    return
                seen.add((x, y))
