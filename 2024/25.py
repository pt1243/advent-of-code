from itertools import groupby, islice

with open("./2024/resources/25.txt") as f:
    text = f.read().strip()


def part_1() -> None:
    keys: list[list[int]] = []
    locks: list[list[int]] = []
    for block in text.split("\n\n"):
        lines = block.split("\n")
        if all(c == "#" for c in lines[0]):
            locks.append([len(list(g)) - 1 for col in zip(*lines) for _, g in islice(groupby(col), 1)])
        else:
            keys.append([len(list(g)) - 1 for col in zip(*lines) for _, g in islice(groupby(col), 1, 2)])
    print(sum(all(lock_pin + key_pin <= 5 for lock_pin, key_pin in zip(lock, key)) for lock in locks for key in keys))
