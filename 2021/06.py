from collections import Counter


with open("./2021/resources/6.txt") as f:
    text = f.read().strip()


def simulate_lanternfish(days: int) -> int:
    current = Counter(int(x) for x in text.split(","))
    for _ in range(days):
        new = Counter()
        for i in range(1, 9):
            new[i - 1] = current[i]
        new[6] += current[0]
        new[8] = current[0]
        current = new
    return current.total()


def problem_1() -> None:
    print(simulate_lanternfish(80))


def problem_2() -> None:
    print(simulate_lanternfish(256))
