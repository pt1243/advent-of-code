with open("./2024/resources/6.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    directions = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
    width = len(lines[0])
    height = len(lines)
    row = next(i for i, line in enumerate(lines) if "^" in line)
    col = lines[row].index("^")
    direction = 0
    seen = {(row, col)}

    while True:
        drow, dcol = directions[direction]
        if not (0 <= row + drow < height) or not (0 <= col + dcol < width):
            break
        if lines[row + drow][col + dcol] == "#":
            direction += 1
            direction %= 4
            continue
        row += drow
        col += dcol
        seen.add((row, col))
    print(len(seen))


def problem_2() -> None:
    directions = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
    width = len(lines[0])
    height = len(lines)
    start_row = next(i for i, line in enumerate(lines) if "^" in line)
    start_col = lines[start_row].index("^")

    def hits_loop(obstacle_row: int, obstacle_col: int) -> bool:
        direction = 0
        row, col = start_row, start_col
        seen = {(row, col, direction)}
        while True:
            drow, dcol = directions[direction]
            if not (0 <= row + drow < height) or not (0 <= col + dcol < width):
                return False
            if lines[row + drow][col + dcol] == "#" or (row + drow == obstacle_row and col + dcol == obstacle_col):
                direction += 1
                direction %= 4
                continue
            row += drow
            col += dcol
            if (row, col, direction) in seen:
                return True
            seen.add((row, col, direction))

    total = 0
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == ".":
                total += hits_loop(row, col)
    print(total)
