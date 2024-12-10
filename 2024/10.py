with open("./2024/resources/10.txt") as f:
    grid = [[int(x) for x in line] for line in f.read().splitlines()]


def problem_1() -> None:
    width, height = len(grid[0]), len(grid)

    def search(start_row: int, start_col: int) -> int:
        open_set = [(start_row, start_col)]
        found: set[tuple[int, int]] = set()
        while open_set:
            row, col = open_set.pop()
            val = grid[row][col]
            if val == 9:
                found.add((row, col))
                continue
            if row > 0 and grid[row - 1][col] == val + 1:
                open_set.append((row - 1, col))
            if row < height - 1 and grid[row + 1][col] == val + 1:
                open_set.append((row + 1, col))
            if col > 0 and grid[row][col - 1] == val + 1:
                open_set.append((row, col - 1))
            if col < width - 1 and grid[row][col + 1] == val + 1:
                open_set.append((row, col + 1))
        return len(found)

    total = 0
    for row, line in enumerate(grid):
        for col, num in enumerate(line):
            if num == 0:
                total += search(row, col)
    print(total)


def problem_2() -> None:
    width, height = len(grid[0]), len(grid)

    def num_paths(start_row: int, start_col: int) -> int:
        open_set = [[(start_row, start_col)]]
        found: set[tuple[tuple[int, int], ...]] = set()
        while open_set:
            path = open_set.pop()
            row, col = path[-1]
            val = grid[row][col]
            if val == 9:
                found.add(tuple(path))
                continue
            if row > 0 and grid[row - 1][col] == val + 1:
                open_set.append(path + [(row - 1, col)])
            if row < height - 1 and grid[row + 1][col] == val + 1:
                open_set.append(path + [(row + 1, col)])
            if col > 0 and grid[row][col - 1] == val + 1:
                open_set.append(path + [(row, col - 1)])
            if col < width - 1 and grid[row][col + 1] == val + 1:
                open_set.append(path + [(row, col + 1)])
        return len(found)

    total = 0
    for row, line in enumerate(grid):
        for col, num in enumerate(line):
            if num == 0:
                total += num_paths(row, col)
    print(total)
