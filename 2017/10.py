from functools import reduce
from itertools import batched
from operator import xor


with open('./2017/resources/10.txt') as f:
    input_text = f.read().strip()


def knot_hash(lst: list[int], lengths: list[int], current_pos: int, skip_size: int) -> tuple[list[int], int, int]:
    num_elements = len(lst)
    for length in lengths:
        for i in range(length // 2):
            idx1, idx2 = (i + current_pos) % num_elements, (current_pos + length - i - 1) % num_elements
            lst[idx1], lst[idx2] = lst[idx2], lst[idx1]
        current_pos += length + skip_size
        current_pos %= num_elements
        skip_size += 1
    return lst, current_pos, skip_size


def problem_1() -> None:
    input_lengths = [int(n) for n in input_text.split(",")]
    lst = list(range(256))
    result, *_ = knot_hash(lst, input_lengths, 0, 0)
    print(result[0] * result[1])


def problem_2() -> None:
    lst = list(range(256))
    lengths = [ord(c) for c in input_text]
    lengths += [17, 31, 73, 47, 23]
    current_pos, skip_size = 0, 0
    for _ in range(64):
        lst, current_pos, skip_size = knot_hash(lst, lengths, current_pos, skip_size)
    block_xors: list[int] = []
    for block in batched(lst, 16):
        block_xors.append(reduce(xor, block))
    print("".join(hex(b)[2:] for b in block_xors))
