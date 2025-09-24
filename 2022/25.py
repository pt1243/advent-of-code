with open("./2022/resources/25.txt") as f:
    lines = f.read().splitlines()


def decimal_to_snafu(number: int) -> str:
    exponent = 1
    while abs(number) > (5**exponent) // 2:
        exponent += 1
    exponent -= 1
    snafu_digits = []
    while exponent >= 0:
        place_value = 5**exponent
        max_distance = place_value // 2
        for digit in range(-2, 3):
            value = digit * place_value
            if abs(number - value) <= max_distance:
                snafu_digits.append(digit)
                number -= value
                break
        exponent -= 1
    lookup = {2: "2", 1: "1", 0: "0", -1: "-", -2: "="}
    return "".join(lookup[digit] for digit in snafu_digits)


def snafu_to_decimal(snafu_number: str) -> int:
    number = 0
    lookup = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
    for exponent, char in enumerate(reversed(snafu_number)):
        number += lookup[char] * 5**exponent
    return number


def problem_1() -> None:
    print(decimal_to_snafu(sum(snafu_to_decimal(line) for line in lines)))
