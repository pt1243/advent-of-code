from typing import Iterator


with open('./2017/resources/15.txt') as f:
    lines = [line.strip() for line in f]


def gen(start: int, factor: int) -> Iterator[int]:
    current = start
    while True:
        current = (current * factor) % 2147483647
        yield current


def gen_criteria(start: int, factor: int, multiple: int) -> Iterator[int]:
    current = start
    while True:
        current = (current * factor) % 2147483647
        if current % multiple != 0:
            continue
        yield current


def problem_1() -> None:
    gen_a = gen(int(lines[0].split()[-1]), 16807)
    gen_b = gen(int(lines[1].split()[-1]), 48271)
    total = 0
    for _ in range(40_000_000):
        a_val, b_val = next(gen_a), next(gen_b)
        a_bits = bin(a_val)[-16:].zfill(16)
        b_bits = bin(b_val)[-16:].zfill(16)
        if a_bits == b_bits:
            total += 1
    print(total)


def problem_2() -> None:
    gen_a = gen_criteria(int(lines[0].split()[-1]), 16807, 4)
    gen_b = gen_criteria(int(lines[1].split()[-1]), 48271, 8)
    total = 0
    for _ in range(5_000_000):
        a_val, b_val = next(gen_a), next(gen_b)
        a_bits = bin(a_val)[-16:].zfill(16)
        b_bits = bin(b_val)[-16:].zfill(16)
        if a_bits == b_bits:
            total += 1
    print(total)
