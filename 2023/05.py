from itertools import batched
from typing import cast

with open("./2023/resources/5.txt") as f:
    input_text = f.read().strip()


def process_transformations(initial_ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    conversions: list[dict[tuple[int, int], int]] = []
    blocks = input_text.split("\n\n")
    for block in blocks[1:]:
        lines = block.split("\n")
        current_conversions: dict[tuple[int, int], int] = {}
        for line in lines[1:]:
            dest_range_start, source_range_start, range_length = (int(x) for x in line.split())
            offset = dest_range_start - source_range_start
            current_conversions[(source_range_start, range_length)] = offset
        conversions.append(current_conversions)

    current_ranges = initial_ranges.copy()

    for conversion_map in conversions:
        transformed: list[tuple[int, int]] = []
        still_to_be_transformed: list[tuple[int, int]] = []
        for (source_range_start, range_length), offset in conversion_map.items():
            source_range_end = source_range_start + range_length - 1
            while current_ranges:
                low, length = current_ranges.pop()
                high = low + length - 1
                if high < source_range_start or low > source_range_end:
                    still_to_be_transformed.append((low, length))
                elif source_range_start <= low and high <= source_range_end:
                    transformed.append((low + offset, length))
                else:
                    num_below = max(source_range_start - low, 0)
                    num_above = max(high - source_range_end, 0)
                    in_range = (max(source_range_start, low) + offset, length - num_above - num_below)
                    transformed.append(in_range)
                    if num_below:
                        still_to_be_transformed.append((low, num_below))
                    if num_above:
                        still_to_be_transformed.append((source_range_end + 1, num_above))
            current_ranges = still_to_be_transformed
            still_to_be_transformed = []
        current_ranges += transformed
    return current_ranges


def problem_1() -> None:
    initial_ranges = [(int(start), 1) for start in input_text.split("\n")[0].split(": ")[1].split()]
    transformed_ranges = process_transformations(initial_ranges)
    print(min(transformed_ranges)[0])


def problem_2() -> None:
    nums = [int(x) for x in input_text.split("\n")[0].split(": ")[1].split()]
    initial_ranges = cast(list[tuple[int, int]], list(batched(nums, 2)))
    transformed_ranges = process_transformations(initial_ranges)
    print(min(transformed_ranges)[0])
