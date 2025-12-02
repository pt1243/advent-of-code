from copy import deepcopy
from typing import Callable

with open("./2018/resources/16.txt") as f:
    text = f.read().strip()


def part_1() -> None:
    samples = text.split("\n\n\n\n")[0]
    opcodes: list[Callable[[dict[int, int], int, int], int]] = [
        lambda r, a, b: r[a] + r[b],  # addr
        lambda r, a, b: r[a] + b,  # addi
        lambda r, a, b: r[a] * r[b],  # mulr
        lambda r, a, b: r[a] * b,  # muli
        lambda r, a, b: r[a] & r[b],  # banr
        lambda r, a, b: r[a] & b,  # bani
        lambda r, a, b: r[a] | r[b],  # borr
        lambda r, a, b: r[a] | b,  # bori
        lambda r, a, b: r[a],  # setr
        lambda r, a, b: a,  # seti
        lambda r, a, b: 1 if a > r[b] else 0,  # gtir
        lambda r, a, b: 1 if r[a] > b else 0,  # gtri
        lambda r, a, b: 1 if r[a] > r[b] else 0,  # gtrr
        lambda r, a, b: 1 if a == r[b] else 0,  # eqir
        lambda r, a, b: 1 if r[a] == b else 0,  # eqri
        lambda r, a, b: 1 if r[a] == r[b] else 0,  # eqrr
    ]

    three_or_more = 0
    for sample in samples.split("\n\n"):
        lines = sample.split("\n")
        registers_before = dict(zip(range(4), (int(x) for x in lines[0][9:19].split(", "))))
        registers_after = dict(zip(range(4), (int(x) for x in lines[2][9:19].split(", "))))
        could_match = 0
        for opcode_function in opcodes:
            registers = registers_before.copy()
            _, a, b, c = (int(x) for x in lines[1].split())
            registers[c] = opcode_function(registers, a, b)
            if registers == registers_after:
                could_match += 1
        if could_match >= 3:
            three_or_more += 1
    print(three_or_more)


def part_2() -> None:
    samples, program = text.split("\n\n\n\n")
    opcodes: list[Callable[[dict[int, int], int, int], int]] = [
        lambda r, a, b: r[a] + r[b],  # addr
        lambda r, a, b: r[a] + b,  # addi
        lambda r, a, b: r[a] * r[b],  # mulr
        lambda r, a, b: r[a] * b,  # muli
        lambda r, a, b: r[a] & r[b],  # banr
        lambda r, a, b: r[a] & b,  # bani
        lambda r, a, b: r[a] | r[b],  # borr
        lambda r, a, b: r[a] | b,  # bori
        lambda r, a, b: r[a],  # setr
        lambda r, a, b: a,  # seti
        lambda r, a, b: 1 if a > r[b] else 0,  # gtir
        lambda r, a, b: 1 if r[a] > b else 0,  # gtri
        lambda r, a, b: 1 if r[a] > r[b] else 0,  # gtrr
        lambda r, a, b: 1 if a == r[b] else 0,  # eqir
        lambda r, a, b: 1 if r[a] == b else 0,  # eqri
        lambda r, a, b: 1 if r[a] == r[b] else 0,  # eqrr
    ]

    opcode_indices = {i: set(range(16)) for i in range(16)}
    for sample in samples.split("\n\n"):
        lines = sample.split("\n")
        registers_before = dict(zip(range(4), (int(x) for x in lines[0][9:19].split(", "))))
        registers_after = dict(zip(range(4), (int(x) for x in lines[2][9:19].split(", "))))
        for i, opcode_function in enumerate(opcodes):
            registers = registers_before.copy()
            opcode, a, b, c = (int(x) for x in lines[1].split())
            registers[c] = opcode_function(registers, a, b)
            if registers != registers_after:
                opcode_indices[opcode].discard(i)

    while any(len(possible_opcodes) > 1 for possible_opcodes in opcode_indices.values()):
        new_opcode_indices = deepcopy(opcode_indices)
        for i, possible_opcodes in opcode_indices.items():
            if len(possible_opcodes) == 1:
                item_to_remove = next(iter(possible_opcodes))
                for j, other_possible_opcodes in new_opcode_indices.items():
                    if i == j:
                        continue
                    other_possible_opcodes.discard(item_to_remove)
        opcode_indices = new_opcode_indices
    opcode_mapping = {k: next(iter(v)) for k, v in opcode_indices.items()}
    registers = {0: 0, 1: 0, 2: 0, 3: 0}
    for line in program.split("\n"):
        opcode, a, b, c = (int(x) for x in line.split())
        registers[c] = opcodes[opcode_mapping[opcode]](registers, a, b)
    print(registers[0])
