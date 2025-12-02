from collections import deque
from itertools import batched, count
from typing import cast

with open("./2024/resources/9.txt") as f:
    nums = [int(x) for x in f.read().strip()]


def problem_1() -> None:
    remaining: deque[int | None] = deque()
    file_ids = count()
    for pair in batched(nums, 2):
        remaining.extend([next(file_ids)] * pair[0])
        if len(pair) == 2:
            remaining.extend([None] * pair[1])

    final_order: list[int] = []
    while remaining:
        current = remaining.popleft()
        if current is None:
            while remaining and remaining[-1] is None:
                remaining.pop()
            if not remaining:
                break
            final_order.append(cast(int, remaining.pop()))
        else:
            final_order.append(current)

    print(sum(i * val for i, val in enumerate(final_order)))


def problem_2() -> None:
    free_space_lengths: dict[int, int] = {}
    file_indices_and_lengths: dict[int, tuple[int, int]] = {}
    file_ids = count()
    index = 0
    for pair in batched(nums, 2):
        file_indices_and_lengths[next(file_ids)] = (index, pair[0])
        index += pair[0]
        if len(pair) == 2:
            free_space_lengths[index] = pair[1]
            index += pair[1]

    max_file_id = next(file_ids) - 1
    for file_id in range(max_file_id, -1, -1):
        index, length = file_indices_and_lengths[file_id]
        first_free_position = min(
            (i for i, val in free_space_lengths.items() if val >= length and i < index), default=None
        )
        if first_free_position is None:
            continue
        file_indices_and_lengths[file_id] = (first_free_position, length)

        destination_space = free_space_lengths.pop(first_free_position)
        if destination_space > length:
            difference = destination_space - length
            free_space_lengths[first_free_position + length] = difference

        free_space_after = free_space_lengths.pop(index + length, None)
        if free_space_after is not None:
            length += free_space_after

        index_before = next((i for i in range(1, 10) if free_space_lengths.get(index - i, 0) == i), None)
        if index_before is not None:
            free_space_before = free_space_lengths.pop(index - index_before)
            length += free_space_before
            index -= index_before

        free_space_lengths[index] = length

    total = 0
    for file_id, (start_index, length) in file_indices_and_lengths.items():
        total += file_id * sum(range(start_index, start_index + length))
    print(total)
