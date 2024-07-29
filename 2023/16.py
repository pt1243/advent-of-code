with open("./2023/resources/16.txt") as f:
    lines = [line.strip() for line in f]


def get_num_energized(starting_row: int, starting_col: int, starting_direction: int) -> int:
    height = len(lines)
    width = len(lines[0])
    directions = ((-1, 0), (0, 1), (1, 0), (0, -1))  # up, right, down, left
    slash_directions = {0: 1, 1: 0, 2: 3, 3: 2}
    backslash_direction = {0: 3, 1: 2, 2: 1, 3: 0}
    active_beams = [(starting_row, starting_col, starting_direction)]
    seen = set(active_beams)
    energized = {(0, 0)}
    while active_beams:
        row, col, direction = active_beams.pop()
        drow, dcol = directions[direction]
        new_row, new_col = row + drow, col + dcol
        if new_row < 0 or new_row >= height or new_col < 0 or new_col >= width:
            continue
        energized.add((new_row, new_col))
        char = lines[new_row][new_col]
        new_beams = []
        if char == "-":
            if direction in (1, 3):
                new_beams.append((new_row, new_col, direction))
            else:
                new_beams.append((new_row, new_col, 1))
                new_beams.append((new_row, new_col, 3))
        elif char == "|":
            if direction in (0, 2):
                new_beams.append((new_row, new_col, direction))
            else:
                new_beams.append((new_row, new_col, 0))
                new_beams.append((new_row, new_col, 2))
        elif char == "/":
            new_direction = slash_directions[direction]
            new_beams.append((new_row, new_col, new_direction))
        elif char == "\\":
            new_direction = backslash_direction[direction]
            new_beams.append((new_row, new_col, new_direction))
        else:
            new_beams.append((new_row, new_col, direction))
        for new_beam in new_beams:
            if new_beam not in seen:
                seen.add(new_beam)
                active_beams.append(new_beam)
    return len(energized)


def problem_1() -> None:
    print(get_num_energized(0, -1, 1))


def problem_2() -> None:
    max_tiles_energized = 0
    for starting_col in range(len(lines[0])):
        top = get_num_energized(-1, starting_col, 2)
        bottom = get_num_energized(len(lines), starting_col, 0)
        max_tiles_energized = max(max_tiles_energized, top, bottom)
    for starting_row in range(len(lines)):
        left = get_num_energized(starting_row, -1, 1)
        right = get_num_energized(starting_row, len(lines[0]), 3)
        max_tiles_energized = max(max_tiles_energized, left, right)
    print(max_tiles_energized)
