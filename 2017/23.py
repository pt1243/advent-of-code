from collections import defaultdict
from math import ceil, sqrt


with open("./2017/resources/23.txt") as f:
    instructions = [line.strip() for line in f]


def problem_1() -> None:
    i = 0
    times_mul_invoked = 0
    registers = defaultdict(int)
    while 0 <= i < len(instructions):
        opcode, reg, src = instructions[i].split()
        try:
            val = int(src)
        except ValueError:
            val = registers[src]
        if opcode == "set":
            registers[reg] = val
            i += 1
        elif opcode == "sub":
            registers[reg] -= val
            i += 1
        elif opcode == "mul":
            registers[reg] *= val
            times_mul_invoked += 1
            i += 1
        else:
            try:
                condition = int(reg)
            except ValueError:
                condition = registers[reg]
            if condition != 0:
                i += val
            else:
                i += 1
    print(times_mul_invoked)


def problem_2() -> None:
    lower_bound = int(instructions[0].split()[2]) * int(instructions[4].split()[2]) - int(instructions[5].split()[2])
    upper_bound = lower_bound - int(instructions[7].split()[2])
    step = -int(instructions[-2].split()[2])
    num_not_prime = 0
    for i in range(lower_bound, upper_bound + 1, step):
        for j in range(2, ceil(sqrt(i)) + 1):
            if i % j == 0:
                num_not_prime += 1
                break
    print(num_not_prime)
