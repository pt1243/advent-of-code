from functools import cache

with open("./2025/resources/11.txt") as f:
    lines = f.read().splitlines()


def part_1() -> None:
    connections: dict[str, list[str]] = {}
    for line in lines:
        left, right = line.split(": ")
        connections[left] = right.split()

    @cache
    def num_paths(current: str) -> int:
        if current == "out":
            return 1
        return sum(num_paths(possible) for possible in connections[current])

    print(num_paths("you"))


def part_2() -> None:
    connections: dict[str, list[str]] = {}
    for line in lines:
        left, right = line.split(": ")
        connections[left] = right.split()

    @cache
    def num_paths(current: str, seen_dac: bool, seen_fft: bool) -> int:
        if current == "out":
            return int(seen_dac and seen_fft)
        if current == "dac":
            seen_dac = True
        if current == "fft":
            seen_fft = True
        return sum(num_paths(possible, seen_dac, seen_fft) for possible in connections[current])

    print(num_paths("svr", False, False))
