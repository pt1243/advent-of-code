with open("./2025/resources/4.txt") as f:
    lines = f.read().splitlines()


def get_paper_to_remove(paper_locations: set[tuple[int, int]]) -> set[tuple[int, int]]:
    to_remove = set()
    for row, col in paper_locations:
        adjacent = (
            ((row - 1, col - 1) in paper_locations)
            + ((row - 1, col) in paper_locations)
            + ((row - 1, col + 1) in paper_locations)
            + ((row, col - 1) in paper_locations)
            + ((row, col + 1) in paper_locations)
            + ((row + 1, col - 1) in paper_locations)
            + ((row + 1, col) in paper_locations)
            + ((row + 1, col + 1) in paper_locations)
        )
        if adjacent < 4:
            to_remove.add((row, col))
    return to_remove


def part_1() -> None:
    paper_locations = {(row, col) for row, line in enumerate(lines) for col, char in enumerate(line) if char == "@"}
    print(len(get_paper_to_remove(paper_locations)))


def part_2() -> None:
    paper_locations = {(row, col) for row, line in enumerate(lines) for col, char in enumerate(line) if char == "@"}
    total_paper_removed = 0
    while True:
        paper_to_remove = get_paper_to_remove(paper_locations)
        if not paper_to_remove:
            print(total_paper_removed)
            return
        total_paper_removed += len(paper_to_remove)
        paper_locations -= paper_to_remove
