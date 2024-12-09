from collections import deque
from itertools import batched, count


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
            final_order.append(remaining.pop())
        else:
            final_order.append(current)

    print(sum(i * val for i, val in enumerate(final_order)))


def problem_2() -> None:  # TODO: speed this up
    disk: list[tuple[int | None, int]] = []
    file_ids = count()
    for pair in batched(nums, 2):
        disk.append((next(file_ids), pair[0]))
        if len(pair) == 2:
            disk.append((None, pair[1]))

    max_file_id_number = next(file_ids) - 1
    for file_id in range(max_file_id_number, -1, -1):
        index, length = next((i, val[1]) for i, val in enumerate(disk) if val[0] == file_id)
        try:
            available_space_index, available_space_length = next(
                (i, val[1]) for i, val in enumerate(disk) if i < index and val[0] is None and val[1] >= length
            )
        except StopIteration:
            continue
        if available_space_length == length:
            disk[available_space_index] = (file_id, length)
        else:
            disk.insert(available_space_index, (file_id, length))
            disk[available_space_index + 1] = (None, available_space_length - length)
            index += 1
        disk[index] = (None, length)
        if disk[index - 1][0] is None:
            length += disk[index - 1][1]
            disk[index - 1 : index + 1] = [(None, length)]
            index -= 1
        if index < len(disk) - 1 and disk[index + 1][0] is None:
            length += disk[index + 1][1]
            disk[index : index + 2] = [(None, length)]

    expanded = []
    for val in disk:
        if val[0] is None:
            expanded.extend([0] * val[1])
        else:
            expanded.extend([val[0]] * val[1])
    print(sum(i * val for i, val in enumerate(expanded)))
