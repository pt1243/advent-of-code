from itertools import product

from more_itertools import split_before

with open("./2020/resources/14.txt") as f:
    lines = f.read().splitlines()


def part_1() -> None:
    memory: dict[int, int] = {}
    for block in split_before(lines, lambda line: line.startswith("mask")):
        mask = list(block[0].split(" = ")[1])
        for line in block[1:]:
            target, initial_value = line.split(" = ")
            target_address = int(target[4:-1])
            value = list(bin(int(initial_value))[2:].zfill(36))
            for i, char in enumerate(mask):
                if char != "X":
                    value[i] = char
            memory[target_address] = int("".join(value), 2)
    print(sum(memory.values()))


def part_2() -> None:
    memory: dict[int, int] = {}
    for block in split_before(lines, lambda line: line.startswith("mask")):
        mask = list(block[0].split(" = ")[1])
        for line in block[1:]:
            target, value_str = line.split(" = ")
            value = int(value_str)
            initial_address = list(bin(int(target[4:-1]))[2:].zfill(36))
            possibilities: list[tuple[str, ...]] = []
            for initial_bit, char in zip(initial_address, mask):
                if char == "0":
                    possibilities.append((initial_bit,))
                elif char == "1":
                    possibilities.append(("1",))
                else:
                    possibilities.append(("0", "1"))
            for address in product(*possibilities):
                memory[int("".join(address), 2)] = value
    print(sum(memory.values()))
