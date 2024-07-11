from collections import defaultdict


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
    pass
