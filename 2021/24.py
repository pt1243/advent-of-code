from collections import defaultdict
from itertools import batched

with open("./2021/resources/24.txt") as f:
    lines = f.read().splitlines()


def run_ALU(part_2: bool = False) -> int:
    comparison_func = min if part_2 else max
    default_value = 10**15 if part_2 else 0

    divisors, a_constants, b_constants = [], [], []
    for group in batched(lines, 18):
        divisors.append(int(group[4].split()[-1]))
        a_constants.append(int(group[5].split()[-1]))
        b_constants.append(int(group[15].split()[-1]))

    optimal_digits_per_z_state = defaultdict[int, int](lambda: default_value)
    optimal_digits_per_z_state[0] = 0
    for block in range(14):
        divisor = divisors[block]
        a = a_constants[block]
        b = b_constants[block]
        new_optimal_digits_per_z_state = defaultdict[int, int](lambda: default_value)
        for current_z, current_digits in optimal_digits_per_z_state.items():
            divided = current_z // divisor
            modulo = current_z % 26
            for digit in range(1, 10):
                z = divided
                if modulo + a != digit:
                    z *= 26
                    z += digit + b
                new_optimal_digits_per_z_state[z] = comparison_func(
                    new_optimal_digits_per_z_state[z], 10 * current_digits + digit
                )
        optimal_digits_per_z_state = new_optimal_digits_per_z_state
    return comparison_func(digits for z, digits in optimal_digits_per_z_state.items() if z == 0)


def part_1() -> None:
    print(run_ALU())


def part_2() -> None:
    print(run_ALU(part_2=True))
