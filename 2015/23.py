with open("./2015/resources/23.txt") as f:
    lines = f.read().splitlines()


def run_instructions(start_a: int, start_b: int) -> tuple[int, int]:
    instruction_pointer = 0
    a, b = start_a, start_b
    while 0 <= instruction_pointer < len(lines):
        instruction = lines[instruction_pointer]
        reg = instruction.split()[1]

        if instruction.startswith("hlf"):
            if reg == "a":
                a //= 2
            else:
                b //= 2
            instruction_pointer += 1

        elif instruction.startswith("tpl"):
            if reg == "a":
                a *= 3
            else:
                b *= 3
            instruction_pointer += 1

        elif instruction.startswith("inc"):
            if reg == "a":
                a += 1
            else:
                b += 1
            instruction_pointer += 1

        elif instruction.startswith("jmp"):
            offset = int(instruction.split()[1])
            instruction_pointer += offset

        elif instruction.startswith("jie"):
            target, offset_str = instruction.split(", ")
            offset = int(offset_str)
            reg = target.split()[1]
            if reg == "a":
                instruction_pointer += offset if a % 2 == 0 else 1
            else:
                instruction_pointer += offset if b % 2 == 0 else 1

        else:
            target, offset_str = instruction.split(", ")
            offset = int(offset_str)
            reg = target.split()[1]
            if reg == "a":
                instruction_pointer += offset if a == 1 else 1
            else:
                instruction_pointer += offset if b == 1 else 1
    return a, b


def problem_1() -> None:
    _, b = run_instructions(0, 0)
    print(b)


def problem_2() -> None:
    _, b = run_instructions(1, 0)
    print(b)
