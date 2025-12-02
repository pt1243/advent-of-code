from collections import defaultdict

from more_itertools import split_when

with open("./2024/resources/12.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    seen: set[tuple[int, int]] = set()
    width, height = len(lines[0]), len(lines)

    def mark_recursive(row: int, col: int, found: set[tuple[int, int]] | None = None) -> set[tuple[int, int]]:
        if found is None:
            found = set()
        char = lines[row][col]
        found.add((row, col))
        seen.add((row, col))
        if row > 0 and lines[row - 1][col] == char and (row - 1, col) not in seen:
            found |= mark_recursive(row - 1, col, found)
        if row < height - 1 and lines[row + 1][col] == char and (row + 1, col) not in seen:
            found |= mark_recursive(row + 1, col, found)
        if col > 0 and lines[row][col - 1] == char and (row, col - 1) not in seen:
            found |= mark_recursive(row, col - 1, found)
        if col < width - 1 and lines[row][col + 1] == char and (row, col + 1) not in seen:
            found |= mark_recursive(row, col + 1, found)

        return found

    regions: list[set[tuple[int, int]]] = []
    for row in range(height):
        for col in range(width):
            if (row, col) not in seen:
                regions.append(mark_recursive(row, col))
    total = 0
    for region in regions:
        perimeter = 0
        for row, col in region:
            if (row - 1, col) not in region:
                perimeter += 1
            if (row + 1, col) not in region:
                perimeter += 1
            if (row, col - 1) not in region:
                perimeter += 1
            if (row, col + 1) not in region:
                perimeter += 1
        total += perimeter * len(region)
    print(total)


def problem_2() -> None:
    seen: set[tuple[int, int]] = set()
    width, height = len(lines[0]), len(lines)

    def mark_recursive(row: int, col: int, found: set[tuple[int, int]] | None = None) -> set[tuple[int, int]]:
        if found is None:
            found = set()
        char = lines[row][col]
        found.add((row, col))
        seen.add((row, col))
        if row > 0 and lines[row - 1][col] == char and (row - 1, col) not in seen:
            found |= mark_recursive(row - 1, col, found)
        if row < height - 1 and lines[row + 1][col] == char and (row + 1, col) not in seen:
            found |= mark_recursive(row + 1, col, found)
        if col > 0 and lines[row][col - 1] == char and (row, col - 1) not in seen:
            found |= mark_recursive(row, col - 1, found)
        if col < width - 1 and lines[row][col + 1] == char and (row, col + 1) not in seen:
            found |= mark_recursive(row, col + 1, found)

        return found

    regions: list[set[tuple[int, int]]] = []
    for row in range(height):
        for col in range(width):
            if (row, col) not in seen:
                regions.append(mark_recursive(row, col))

    total = 0
    for region in regions:
        vertical_edges: defaultdict[int, list[tuple[int, bool]]] = defaultdict(list)
        horizontal_edges: defaultdict[int, list[tuple[int, bool]]] = defaultdict(list)
        for row, col in region:
            if (row - 1, col) not in region:
                horizontal_edges[row].append((col, True))
            if (row + 1, col) not in region:
                horizontal_edges[row + 1].append((col, False))
            if (row, col - 1) not in region:
                vertical_edges[col].append((row, True))
            if (row, col + 1) not in region:
                vertical_edges[col + 1].append((row, False))
        sides = 0
        for same_row in horizontal_edges.values():
            sides += sum(1 for _ in split_when(sorted(same_row), lambda a, b: abs(a[0] - b[0]) > 1 or a[1] != b[1]))
        for same_col in vertical_edges.values():
            sides += sum(1 for _ in split_when(sorted(same_col), lambda a, b: abs(a[0] - b[0]) > 1 or a[1] != b[1]))
        total += sides * len(region)
    print(total)
