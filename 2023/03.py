from collections import defaultdict


with open("./2023/resources/3.txt") as f:
    lines = f.read().splitlines()


def find_number_indices() -> list[tuple[int, int, int]]:
    found_nums: list[tuple[int, int, int]] = []
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if not char.isnumeric():
                continue
            if line[j - 1].isnumeric():
                continue
            end_index = j
            for k, other_char in enumerate(line[j:], start=j):
                if not other_char.isnumeric():
                    break
                end_index = k
            found_nums.append((i, j, end_index))
    return found_nums


def get_positions_to_check(i: int, j: int, k: int, max_char_index: int, max_line_index: int) -> list[tuple[int, int]]:
    positions_to_check: list[tuple[int, int]] = []
    if i != 0:
        positions_to_check.extend(((i - 1, m) for m in range(j, k + 1)))
        if j != 0:
            positions_to_check.append((i - 1, j - 1))
        if k != max_char_index:
            positions_to_check.append((i - 1, k + 1))
    if j != 0:
        positions_to_check.append((i, j - 1))
    if k != max_char_index:
        positions_to_check.append((i, k + 1))
    if i != max_line_index:
        positions_to_check.extend(((i + 1, m) for m in range(j, k + 1)))
        if j != 0:
            positions_to_check.append((i + 1, j - 1))
        if k != max_char_index:
            positions_to_check.append((i + 1, k + 1))
    return positions_to_check


def problem_1() -> None:
    sum_part_nums = 0
    max_line_index = len(lines) - 1
    max_char_index = len(lines[0]) - 1

    found_nums = find_number_indices()

    for i, j, k in found_nums:
        posititions_to_check = get_positions_to_check(i, j, k, max_char_index, max_line_index)
        if any(lines[m][n] != "." and not lines[m][n].isnumeric() for m, n in posititions_to_check):
            sum_part_nums += int("".join(lines[i][j : k + 1]))

    print(sum_part_nums)


def problem_2() -> None:
    total_ratio = 0
    max_line_index = len(lines) - 1
    max_char_index = len(lines[0]) - 1

    found_nums = find_number_indices()

    gears: defaultdict[tuple[int, int], list[int]] = defaultdict(list)
    for i, j, k in found_nums:
        positions_to_check = get_positions_to_check(i, j, k, max_char_index, max_line_index)

        for m, n in positions_to_check:
            if lines[m][n] == "*":
                gears[(m, n)].append(int("".join(lines[i][j : k + 1])))

    for list_nums in gears.values():
        if len(list_nums) == 2:
            total_ratio += list_nums[0] * list_nums[1]

    print(total_ratio)
