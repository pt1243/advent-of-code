with open("./2016/resources/23.txt") as f:
    instructions = f.read().splitlines()


def run_instructions(registers: dict[str, int]) -> dict[str, int]:
    i = 0
    while 0 <= i < len(instructions):
        current = instructions[i]
        if current.startswith("tgl"):
            offset = int(current.split()[1]) if current.split()[1].isnumeric() else registers[current.split()[1]]
            target_index = i + offset
            if target_index < 0 or target_index >= len(instructions):
                i += 1
                continue
            target = instructions[target_index]
            split = target.split()
            if len(split) == 2:
                if split[0] == "inc":
                    instructions[target_index] = f"dec {split[1]}"
                else:
                    instructions[target_index] = f"inc {split[1]}"
            else:
                if split[0] == "jnz":
                    instructions[target_index] = f"cpy {split[1]} {split[2]}"
                else:
                    instructions[target_index] = f"jnz {split[1]} {split[2]}"
            i += 1
        elif current.startswith("cpy"):
            i += 1
            split = current.split()
            value = split[1]
            target = split[2]
            if not target.isalpha():
                continue
            registers[target] = int(value) if value.isnumeric() or value.startswith("-") else registers[value]
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
            jump = int(split[2]) if split[2].isnumeric() or split[2].startswith("-") else registers[split[2]]
            i += jump if condition != 0 else 1
    return registers


def part_1() -> None:
    registers = {
        "a": 7,
        "b": 0,
        "c": 0,
        "d": 0,
    }

    result = run_instructions(registers)
    print(result["a"])


def part_2() -> None:
    a = 12
    for b in range(11, 0, -1):
        a *= b
    c = int(instructions[-7].split()[1])
    d = int(instructions[-6].split()[1])
    a += c * d
    print(a)
