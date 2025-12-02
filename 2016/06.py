from collections import Counter

with open("./2016/resources/6.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    print("".join(Counter(col).most_common(1)[0][0] for col in zip(*lines)))


def problem_2() -> None:
    print("".join(Counter(col).most_common()[-1][0] for col in zip(*lines)))
