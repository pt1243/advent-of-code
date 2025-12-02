from typing import Generator

with open("./2017/resources/15.txt") as f:
    lines = f.read().splitlines()


def gen(start: int, factor: int) -> Generator[int, None, None]:
    current = start
    while True:
        current = (current * factor) % 2147483647
        yield current


def gen_criteria(start: int, factor: int, multiple: int) -> Generator[int, None, None]:
    current = start
    while True:
        current = (current * factor) % 2147483647
        if current % multiple != 0:
            continue
        yield current


def part_1() -> None:
    gen_a = gen(int(lines[0].split()[-1]), 16807)
    gen_b = gen(int(lines[1].split()[-1]), 48271)
    total = 0
    for _ in range(40_000_000):
        if (next(gen_a) & 65535) == (next(gen_b) & 65535):
            total += 1
    print(total)


def part_2() -> None:
    gen_a = gen_criteria(int(lines[0].split()[-1]), 16807, 4)
    gen_b = gen_criteria(int(lines[1].split()[-1]), 48271, 8)
    total = 0
    for _ in range(5_000_000):
        if (next(gen_a) & 65535) == (next(gen_b) & 65535):
            total += 1
    print(total)
