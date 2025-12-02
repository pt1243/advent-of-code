with open("./2024/resources/17.txt") as f:
    lines = f.read().splitlines()


def run_program(A: int, B: int, C: int, program: list[int]) -> list[int]:
    outputs: list[int] = []

    def get_combo_operand_value(operand: int) -> int:
        if 0 <= operand <= 3:
            return operand
        if operand == 4:
            return A
        if operand == 5:
            return B
        if operand == 6:
            return C
        raise ValueError(f"invalid combo operand {operand}")

    i = 0
    while 0 <= i < len(program):
        opcode = program[i]
        operand = program[i + 1]
        if opcode == 0:  # adv
            A //= 2 ** get_combo_operand_value(operand)
        elif opcode == 1:  # bxl
            B ^= operand
        elif opcode == 2:  # bst
            B = get_combo_operand_value(operand) % 8
        elif opcode == 3:  # jnz
            if A != 0:
                i = operand
                continue
        elif opcode == 4:  # bxc
            B ^= C
        elif opcode == 5:  # out
            outputs.append(get_combo_operand_value(operand) % 8)
        elif opcode == 6:  # bdv
            B = A // (2 ** get_combo_operand_value(operand))
        elif opcode == 7:  # cdv
            C = A // (2 ** get_combo_operand_value(operand))
        else:
            raise ValueError(f"invalid opcode {opcode}")
        i += 2
    return outputs


def part_1() -> None:
    A = int(lines[0].split(": ")[1])
    B = int(lines[1].split(": ")[1])
    C = int(lines[2].split(": ")[1])
    program = [int(x) for x in lines[4].split(": ")[1].split(",")]
    print(",".join(str(x) for x in run_program(A, B, C, program)))


def part_2() -> None:
    B = int(lines[1].split(": ")[1])
    C = int(lines[2].split(": ")[1])
    program = [int(x) for x in lines[4].split(": ")[1].split(",")]

    def call_recursive(start: int) -> bool:
        for i in range(8):
            output = run_program(start + i, B, C, program)
            pos = len(output)
            if program[-pos] == output[0]:
                if len(output) == len(program):  # cannot recurse further
                    print(start + i)
                    return output == program
                if call_recursive((start + i) << 3):
                    return True
        return False

    call_recursive(0)
