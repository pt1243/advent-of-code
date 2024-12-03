import re


with open("./2024/resources/3.txt") as f:
    text = f.read().strip()


def problem_1() -> None:
    pattern = re.compile(r"mul\((-?\d+),(-?\d+)\)")
    print(sum(int(match[0]) * int(match[1]) for match in re.findall(pattern, text)))


def problem_2() -> None:
    pattern = re.compile(r"mul\((-?\d+),(-?\d+)\)|(do\(\))|(don't\(\))")
    enabled = True
    total = 0
    for match in re.findall(pattern, text):
        if match[2]:
            enabled = True
        elif match[3]:
            enabled = False
        elif enabled:
            total += int(match[0]) * int(match[1])
    print(total)
