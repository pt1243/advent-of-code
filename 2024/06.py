with open("./2024/resources/6.txt") as f:
    lines = f.read().splitlines()


def get_visited_tiles() -> set[tuple[int, int]]:
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
    return seen


def problem_1() -> None:
    print(len(get_visited_tiles()))


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
                if (row, col, direction) in seen:
                    return True
                seen.add((row, col, direction))
                continue
            row += drow
            col += dcol

    print(sum(hits_loop(row, col) for (row, col) in get_visited_tiles()))
