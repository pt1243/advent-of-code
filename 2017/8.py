from collections import defaultdict
import operator


with open('./2017/resources/8.txt') as f:
    lines = [line.strip() for line in f]


def problem_1() -> None:
    registers: defaultdict[str, int] = defaultdict(int)
    operators = {
        "<": operator.lt,
        "<=": operator.le,
        ">": operator.gt,
        ">=": operator.ge,
        "==": operator.eq,
        "!=": operator.ne,
    }

    for line in lines:
        split = line.split()
        condition_target = split[4]
        condition_operator = operators[split[5]]
        condition_value = int(split[6])
        if condition_operator(registers[condition_target], condition_value):
            target = split[0]
            value = int(split[2])
            multiplier = 1 if split[1] == "inc" else -1
            registers[target] += multiplier * value

    print(max(registers.values()))


def problem_2() -> None:
    registers: defaultdict[str, int] = defaultdict(int)
    operators = {
        "<": operator.lt,
        "<=": operator.le,
        ">": operator.gt,
        ">=": operator.ge,
        "==": operator.eq,
        "!=": operator.ne,
    }
    max_seen = 0

    for line in lines:
        split = line.split()
        condition_target = split[4]
        condition_operator = operators[split[5]]
        condition_value = int(split[6])
        if condition_operator(registers[condition_target], condition_value):
            target = split[0]
            value = int(split[2])
            multiplier = 1 if split[1] == "inc" else -1
            registers[target] += multiplier * value
        max_seen = max(max_seen, max(registers.values()))

    print(max_seen)
