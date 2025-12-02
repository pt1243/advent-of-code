with open("./2021/resources/9.txt") as f:
    lines = f.read().splitlines()


def part_1() -> None:
    height = len(lines)
    width = len(lines[0])
    sum_of_risk_levels = 0
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            low_point = True
            if row > 0 and lines[row - 1][col] <= char:
                low_point = False
            if row < height - 1 and lines[row + 1][col] <= char:
                low_point = False
            if col > 0 and lines[row][col - 1] <= char:
                low_point = False
            if col < width - 1 and lines[row][col + 1] <= char:
                low_point = False
            if low_point:
                sum_of_risk_levels += int(char) + 1
    print(sum_of_risk_levels)


def part_2() -> None:
    height = len(lines)
    width = len(lines[0])

    def basin_size(starting_row: int, starting_col: int) -> int:
        seen: set[tuple[int, int]] = set()
        queue = [(starting_row, starting_col)]
        while queue:
            row, col = queue.pop()
            if (row, col) in seen:
                continue
            seen.add((row, col))
            if row > 0 and lines[row - 1][col] < "9":
                queue.append((row - 1, col))
            if row < height - 1 and lines[row + 1][col] < "9":
                queue.append((row + 1, col))
            if col > 0 and lines[row][col - 1] < "9":
                queue.append((row, col - 1))
            if col < width - 1 and lines[row][col + 1] < "9":
                queue.append((row, col + 1))
        return len(seen)

    basin_sizes: list[int] = []
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            low_point = True
            if row > 0 and lines[row - 1][col] <= char:
                low_point = False
            if row < height - 1 and lines[row + 1][col] <= char:
                low_point = False
            if col > 0 and lines[row][col - 1] <= char:
                low_point = False
            if col < width - 1 and lines[row][col + 1] <= char:
                low_point = False
            if low_point:
                basin_sizes.append(basin_size(row, col))

    basin_sizes.sort(reverse=True)
    print(basin_sizes[0] * basin_sizes[1] * basin_sizes[2])
