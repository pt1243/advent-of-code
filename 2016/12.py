with open('./2016/resources/12.txt') as f:
    instructions = [line.strip() for line in f]


def run_instructions(registers: dict[str, int]) -> dict[str, int]:
    i = 0
    while 0 <= i < len(instructions):
        current = instructions[i]
        # print(f"{current = }")
        if current.startswith("cpy"):
            i += 1
            split = current.split()
            value = split[1]
            target = split[2]
            registers[target] = int(value) if value.isnumeric() else registers[value]
        elif current.startswith("inc"):
            i += 1
            target = current.split()[1]
            registers[target] += 1
        elif current.startswith("dec"):
            i += 1
            target = current.split()[1]
            registers[target] -= 1
        else:
            split = current.split()
            condition = int(split[1]) if split[1].isnumeric() else registers[split[1]]
            jump = int(split[2])
            i += jump if condition != 0 else 1
    return registers


def problem_1() -> None:
    registers = {
        "a": 0,
        "b": 0,
        "c": 0,
        "d": 0,
    }

    result = run_instructions(registers)
    print(result["a"])


def problem_2() -> None:
    registers = {
        "a": 0,
        "b": 0,
        "c": 1,
        "d": 0,
    }

    result = run_instructions(registers)
    print(result["a"])
