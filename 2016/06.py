from collections import Counter


with open("./2016/resources/6.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    counters: list[Counter[str]] = [Counter() for _ in lines[0]]

    for line in lines:
        for idx, char in enumerate(line):
            counters[idx].update((char,))

    print("".join(c.most_common(1)[0][0] for c in counters))


def problem_2() -> None:
    counters: list[Counter[str]] = [Counter() for _ in lines[0]]

    for line in lines:
        for idx, char in enumerate(line):
            counters[idx].update((char,))

    print("".join(c.most_common()[-1][0] for c in counters))
