import re
from functools import cache
from typing import cast

with open("./2020/resources/19.txt") as f:
    text = f.read().strip()


def part_1() -> None:
    parsed_rules: dict[int, list[list[int | str]]] = {}
    lines, messages = text.split("\n\n")
    for line in lines.split("\n"):
        left, right = line.split(": ")
        options = []
        for option in right.split(" | "):
            sequence: list[int | str] = []
            for num in option.split():
                if "a" in num or "b" in num:
                    sequence.append(num.strip('"'))
                else:
                    sequence.append(int(num))
            options.append(sequence)
        parsed_rules[int(left)] = options

    @cache
    def get_regex_string(rule: int) -> str:
        if isinstance(parsed_rules[rule][0][0], int):
            return (
                "(?:"
                + "|".join("".join(get_regex_string(item) for item in option) for option in parsed_rules[rule])
                + ")"
            )
        else:
            return cast(str, parsed_rules[rule][0][0])

    pattern = re.compile(get_regex_string(0))
    total = 0
    for message in messages.split("\n"):
        if re.fullmatch(pattern, message):
            total += 1
    print(total)


def part_2() -> None:
    parsed_rules: dict[int, list[list[int | str]]] = {}
    lines, messages = text.split("\n\n")
    for line in lines.split("\n"):
        left, right = line.split(": ")
        options = []
        for option in right.split(" | "):
            sequence: list[int | str] = []
            for num in option.split():
                if "a" in num or "b" in num:
                    sequence.append(num.strip('"'))
                else:
                    sequence.append(int(num))
            options.append(sequence)
        parsed_rules[int(left)] = options

    @cache
    def get_regex_string(rule: int) -> str:
        if rule == 8:
            return "(?:" + get_regex_string(42) + "+)"
        if rule == 11:
            return "(?:" + "|".join(get_regex_string(42) * i + get_regex_string(31) * i for i in range(1, 20)) + ")"
        if isinstance(parsed_rules[rule][0][0], int):
            return (
                "(?:"
                + "|".join("".join(get_regex_string(item) for item in option) for option in parsed_rules[rule])
                + ")"
            )
        else:
            return cast(str, parsed_rules[rule][0][0])

    pattern = re.compile(get_regex_string(0))
    total = 0
    for message in messages.split("\n"):
        if re.fullmatch(pattern, message):
            total += 1
    print(total)
