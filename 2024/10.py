with open("./2024/resources/10.txt") as f:
    grid = [[int(x) for x in line] for line in f.read().splitlines()]


def find_paths(start_row: int, start_col: int) -> tuple[int, int]:
    width, height = len(grid[0]), len(grid)
    open_set = [(start_row, start_col)]
    num_paths = 0
    end_points: set[tuple[int, int]] = set()
    while open_set:
        row, col = open_set.pop()
        val = grid[row][col]
        if val == 9:
            num_paths += 1
            end_points.add((row, col))
            continue
        if row > 0 and grid[row - 1][col] == val + 1:
            open_set.append((row - 1, col))
        if row < height - 1 and grid[row + 1][col] == val + 1:
            open_set.append((row + 1, col))
        if col > 0 and grid[row][col - 1] == val + 1:
            open_set.append((row, col - 1))
        if col < width - 1 and grid[row][col + 1] == val + 1:
            open_set.append((row, col + 1))
    return len(end_points), num_paths


def part_1() -> None:
    total = 0
    for row, line in enumerate(grid):
        for col, num in enumerate(line):
            if num == 0:
                total += find_paths(row, col)[0]
    print(total)


def part_2() -> None:
    total = 0
    for row, line in enumerate(grid):
        for col, num in enumerate(line):
            if num == 0:
                total += find_paths(row, col)[1]
    print(total)
