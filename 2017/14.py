from collections import defaultdict
from functools import reduce
from itertools import batched
from operator import xor


with open("./2017/resources/14.txt") as f:
    key_string = f.read().strip()


def knot_hash(text: str) -> str:
    lengths = [ord(c) for c in text] + [17, 31, 73, 47, 23]
    lst, num_elements = list(range(256)), 256
    current_pos, skip_size = 0, 0

    for _ in range(64):
        for length in lengths:
            for i in range(length // 2):
                idx1, idx2 = (i + current_pos) % num_elements, (current_pos + length - i - 1) % num_elements
                lst[idx1], lst[idx2] = lst[idx2], lst[idx1]
            current_pos += length + skip_size
            current_pos %= num_elements
            skip_size += 1

    blocks: list[int] = [reduce(xor, block) for block in batched(lst, 16)]
    return "".join(hex(b)[2:].zfill(2) for b in blocks)


def problem_1() -> None:
    total_used = 0
    for i in range(128):
        hex_string = knot_hash(f"{key_string}-{i}")
        binary_string = "".join(bin(int(c, 16))[2:].zfill(4) for c in hex_string)
        num_positions = binary_string.count("1")
        total_used += num_positions
    print(total_used)


def problem_2() -> None:
    groups: defaultdict[tuple[int, int], int] = defaultdict(int)
    all_squares: list[str] = []
    for i in range(128):
        hex_string = knot_hash(f"{key_string}-{i}")
        binary_string = "".join(bin(int(c, 16))[2:].zfill(4) for c in hex_string)
        all_squares.append(binary_string)

    def mark_recursive(row: int, col: int, group: int) -> None:
        groups[(row, col)] = group
        if row > 0 and all_squares[row - 1][col] == "1" and not groups[(row - 1, col)]:
            mark_recursive(row - 1, col, group)
        if row < 127 and all_squares[row + 1][col] == "1" and not groups[(row + 1, col)]:
            mark_recursive(row + 1, col, group)
        if col > 0 and all_squares[row][col - 1] == "1" and not groups[(row, col - 1)]:
            mark_recursive(row, col - 1, group)
        if col < 127 and all_squares[row][col + 1] == "1" and not groups[(row, col + 1)]:
            mark_recursive(row, col + 1, group)

    for row, row_list in enumerate(all_squares):
        for col, char in enumerate(row_list):
            if char == "1" and not groups[(row, col)]:
                mark_recursive(row, col, max(groups.values()) + 1)

    print(max(groups.values()))
