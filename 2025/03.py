from functools import cache

with open("./2025/resources/3.txt") as f:
    lines = f.read().splitlines()


@cache
def highest_joltage(available_banks: str, num_digits: int) -> str:
    if num_digits == 1:
        return max(available_banks)
    return max(
        digit + highest_joltage(available_banks[i + 1 :], num_digits - 1)
        for i, digit in enumerate(available_banks[: len(available_banks) - num_digits + 1])
    )


def part_1() -> None:
    print(sum(int(highest_joltage(line, 2)) for line in lines))


def part_2() -> None:
    print(sum(int(highest_joltage(line, 12)) for line in lines))
