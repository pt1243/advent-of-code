with open("./2019/resources/3.txt") as f:
    lines = f.read().splitlines()


def part_1() -> None:
    directions = {"U": (-1, 0), "R": (0, 1), "D": (1, 0), "L": (0, -1)}
    first_wire_seen: set[tuple[int, int]] = set()
    second_wire_seen: set[tuple[int, int]] = set()

    row, col = 0, 0
    for movement in lines[0].split(","):
        direction = movement[0]
        distance = int(movement[1:])
        drow, dcol = directions[direction]
        for _ in range(distance):
            row += drow
            col += dcol
            first_wire_seen.add((row, col))

    row, col = 0, 0
    for movement in lines[1].split(","):
        direction = movement[0]
        distance = int(movement[1:])
        drow, dcol = directions[direction]
        for _ in range(distance):
            row += drow
            col += dcol
            second_wire_seen.add((row, col))

    print(min(abs(p[0]) + abs(p[1]) for p in first_wire_seen & second_wire_seen))


def part_2() -> None:
    directions = {"U": (-1, 0), "R": (0, 1), "D": (1, 0), "L": (0, -1)}
    first_wire_seen: set[tuple[int, int]] = set()
    first_wire_steps: dict[tuple[int, int], int] = {}
    second_wire_seen: set[tuple[int, int]] = set()
    second_wire_steps: dict[tuple[int, int], int] = {}

    row, col, steps = 0, 0, 0
    for movement in lines[0].split(","):
        direction = movement[0]
        distance = int(movement[1:])
        drow, dcol = directions[direction]
        for _ in range(distance):
            row += drow
            col += dcol
            steps += 1
            first_wire_seen.add((row, col))
            if (row, col) not in first_wire_steps:
                first_wire_steps[(row, col)] = steps

    row, col, steps = 0, 0, 0
    for movement in lines[1].split(","):
        direction = movement[0]
        distance = int(movement[1:])
        drow, dcol = directions[direction]
        for _ in range(distance):
            row += drow
            col += dcol
            steps += 1
            second_wire_seen.add((row, col))
            if (row, col) not in second_wire_steps:
                second_wire_steps[(row, col)] = steps

    print(min(first_wire_steps[p] + second_wire_steps[p] for p in first_wire_seen & second_wire_seen))
