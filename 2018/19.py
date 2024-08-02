from collections import Counter
from itertools import count, product
from typing import Callable, Mapping


with open("./2018/resources/19.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    registers = {i: 0 for i in range(6)}
    ip_register = int(lines[0].split()[1])
    instructions = lines[1:]
    opcodes: dict[str, Callable[[Mapping[int, int], int, int], int]] = {
        "addr": lambda r, a, b: r[a] + r[b],  # addr
        "addi": lambda r, a, b: r[a] + b,  # addi
        "mulr": lambda r, a, b: r[a] * r[b],  # mulr
        "muli": lambda r, a, b: r[a] * b,  # muli
        "banr": lambda r, a, b: r[a] & r[b],  # banr
        "bani": lambda r, a, b: r[a] & b,  # bani
        "borr": lambda r, a, b: r[a] | r[b],  # borr
        "bori": lambda r, a, b: r[a] | b,  # bori
        "setr": lambda r, a, b: r[a],  # setr
        "seti": lambda r, a, b: a,  # seti
        "gtir": lambda r, a, b: 1 if a > r[b] else 0,  # gtir
        "gtri": lambda r, a, b: 1 if r[a] > b else 0,  # gtri
        "gtrr": lambda r, a, b: 1 if r[a] > r[b] else 0,  # gtrr
        "eqir": lambda r, a, b: 1 if a == r[b] else 0,  # eqir
        "eqri": lambda r, a, b: 1 if r[a] == b else 0,  # eqri
        "eqrr": lambda r, a, b: 1 if r[a] == r[b] else 0,  # eqrr
    }
    i = 0
    while 0 <= i < len(instructions):
        instruction = instructions[i]
        registers[ip_register] = i
        opcode = instruction.split()[0]
        a, b, c = (int(x) for x in instruction.split()[1:])
        registers[c] = opcodes[opcode](registers, a, b)
        i = registers[ip_register]
        i += 1
    print(registers[0])


def problem_2() -> None:
    registers = {i: 0 for i in range(6)}
    registers[0] = 1
    ip_register = int(lines[0].split()[1])
    instructions = lines[1:]
    opcodes: dict[str, Callable[[Mapping[int, int], int, int], int]] = {
        "addr": lambda r, a, b: r[a] + r[b],  # addr
        "addi": lambda r, a, b: r[a] + b,  # addi
        "mulr": lambda r, a, b: r[a] * r[b],  # mulr
        "muli": lambda r, a, b: r[a] * b,  # muli
        "banr": lambda r, a, b: r[a] & r[b],  # banr
        "bani": lambda r, a, b: r[a] & b,  # bani
        "borr": lambda r, a, b: r[a] | r[b],  # borr
        "bori": lambda r, a, b: r[a] | b,  # bori
        "setr": lambda r, a, b: r[a],  # setr
        "seti": lambda r, a, b: a,  # seti
        "gtir": lambda r, a, b: 1 if a > r[b] else 0,  # gtir
        "gtri": lambda r, a, b: 1 if r[a] > b else 0,  # gtri
        "gtrr": lambda r, a, b: 1 if r[a] > r[b] else 0,  # gtrr
        "eqir": lambda r, a, b: 1 if a == r[b] else 0,  # eqir
        "eqri": lambda r, a, b: 1 if r[a] == b else 0,  # eqri
        "eqrr": lambda r, a, b: 1 if r[a] == r[b] else 0,  # eqrr
    }
    i = 0
    while 0 <= i < len(instructions):
        instruction = instructions[i]
        if i == 35:
            break
        registers[ip_register] = i
        opcode = instruction.split()[0]
        a, b, c = (int(x) for x in instruction.split()[1:])
        registers[c] = opcodes[opcode](registers, a, b)
        i = registers[ip_register]
        i += 1
    number = registers[1]
    prime_factors: list[int] = []
    while number != 1:
        for i in count(2):
            if number % i == 0:
                prime_factors.append(i)
                number //= i
                break
    counts = Counter(prime_factors)
    unique_prime_factors = sorted(set(prime_factors))
    all_factors: set[int] = set()
    for powers in product(*[range(c + 1) for c in counts.values()]):
        prod = 1
        for i, power in enumerate(powers):
            prod *= unique_prime_factors[i] ** power
        all_factors.add(prod)
    print(sum(all_factors))
