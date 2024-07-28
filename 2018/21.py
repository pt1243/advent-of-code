from __future__ import annotations
from typing import Generator


with open("./2018/resources/21.txt") as f:
    lines = [line.strip() for line in f]


def run_program() -> Generator[int]:
    input_num = int(lines[8].split()[1])
    r4 = 0
    while True:
        r3 = r4 | 65536
        r4 = input_num
        while True:
            r4 += r3 & 255
            r4 = ((r4 & 16777215) * 65899) & 16777215
            if 256 > r3:
                break
            r3 //= 256
        yield r4


def problem_1() -> None:
    program = run_program()
    print(next(program))


def problem_2() -> None:
    program = run_program()
    seen = []
    while True:
        val = next(program)
        if val in seen:
            print(seen[-1])
            return
        seen.append(val)
