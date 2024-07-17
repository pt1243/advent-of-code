from itertools import cycle


with open("./2018/resources/1.txt") as f:
    lines = [int(line.strip()) for line in f]


def problem_1() -> None:
    print(sum(lines))


def problem_2() -> None:
    seen: set[int] = set()
    total = 0
    repeating_frequencies = cycle(lines)
    while True:
        frequency = next(repeating_frequencies)
        total += frequency
        if total in seen:
            print(total)
            return
        seen.add(total)
