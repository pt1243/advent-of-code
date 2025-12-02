with open("./2023/resources/11.txt") as f:
    lines = f.read().splitlines()


def part_1() -> None:
    galaxies: list[tuple[int, int]] = []
    empty_rows: set[int] = set()

    for row, line in enumerate(lines):
        if all(c == "." for c in line):
            empty_rows.add(row)
            continue
        for col, char in enumerate(line):
            if char == "#":
                galaxies.append((row, col))

    empty_cols = {i for i in range(len(lines[0])) if not any(x[1] == i for x in galaxies)}

    total_distance = 0
    for i, g1 in enumerate(galaxies):
        r1, c1 = g1
        for g2 in galaxies[i + 1 :]:
            r2, c2 = g2
            dist = abs(r1 - r2) + abs(c1 - c2)
            upper_row = r1 if r1 >= r2 else r2
            lower_row = r2 if upper_row == r1 else r1
            upper_col = c1 if c1 >= c2 else c2
            lower_col = c2 if upper_col == c1 else c1
            additional_rows = {row for row in empty_rows if lower_row < row < upper_row}
            additional_cols = {col for col in empty_cols if lower_col < col < upper_col}
            total_distance += dist + len(additional_rows) + len(additional_cols)
    print(total_distance)


def part_2() -> None:
    galaxies: list[tuple[int, int]] = []
    empty_rows: set[int] = set()

    for row, line in enumerate(lines):
        if all(c == "." for c in line):
            empty_rows.add(row)
            continue
        for col, char in enumerate(line):
            if char == "#":
                galaxies.append((row, col))

    empty_cols = {i for i in range(len(lines[0])) if not any(x[1] == i for x in galaxies)}

    total_distance = 0
    for i, g1 in enumerate(galaxies):
        r1, c1 = g1
        for g2 in galaxies[i + 1 :]:
            r2, c2 = g2
            dist = abs(r1 - r2) + abs(c1 - c2)
            upper_row = r1 if r1 >= r2 else r2
            lower_row = r2 if upper_row == r1 else r1
            upper_col = c1 if c1 >= c2 else c2
            lower_col = c2 if upper_col == c1 else c1
            additional_rows = {row for row in empty_rows if lower_row < row < upper_row}
            additional_cols = {col for col in empty_cols if lower_col < col < upper_col}
            total_distance += dist + 999999 * len(additional_rows) + 999999 * len(additional_cols)
    print(total_distance)
