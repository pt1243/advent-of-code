from typing import cast

with open("./2025/resources/5.txt") as f:
    text = f.read().strip()


def part_1() -> None:
    all_ranges, ingredients = text.split("\n\n")
    ranges = cast(list[tuple[int, int]], [tuple(map(int, line.split("-"))) for line in all_ranges.split("\n")])
    total = 0
    for ingredient in map(int, ingredients.split("\n")):
        total += any(lower <= ingredient <= upper for (lower, upper) in ranges)
    print(total)


def part_2() -> None:
    ranges = text.split("\n\n")[0]
    to_process = cast(list[tuple[int, int]], [tuple(map(int, line.split("-"))) for line in ranges.split("\n")])
    processed: list[tuple[int, int]] = []
    while to_process:
        current_range = to_process.pop()
        for i, existing_range in enumerate(processed):
            if current_range[0] > existing_range[1] or existing_range[0] > current_range[1]:  # no overlap
                continue
            # remove existing range from processed, add combined range to list to be processed
            processed.pop(i)
            to_process.append((min(current_range[0], existing_range[0]), max(current_range[1], existing_range[1])))
            break
        else:  # no overlaps with any existing ranges, add to processed
            processed.append(current_range)
    print(sum(upper - lower + 1 for (lower, upper) in processed))
