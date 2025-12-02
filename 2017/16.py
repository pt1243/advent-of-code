from itertools import count

with open("./2017/resources/16.txt") as f:
    steps = f.read().strip().split(",")


def dance(start: list[str]) -> list[str]:
    programs = start
    for step in steps:
        if step.startswith("s"):
            end_size = int(step[1:])
            programs = programs[-end_size:] + programs[: 16 - end_size]
        elif step.startswith("x"):
            index_strings = step[1:].split("/")
            idx_a, idx_b = int(index_strings[0]), int(index_strings[1])
            programs[idx_a], programs[idx_b] = programs[idx_b], programs[idx_a]
        else:
            a, b = step[1], step[3]
            idx_a = programs.index(a)
            idx_b = programs.index(b)
            programs[idx_a], programs[idx_b] = programs[idx_b], programs[idx_a]
    return programs


def part_1() -> None:
    programs = [chr(i + 97) for i in range(16)]
    print("".join(dance(programs)))


def part_2() -> None:
    positions_seen: dict[int, str] = {}
    programs = [chr(i + 97) for i in range(16)]
    for i in count(1):
        programs = dance(programs)
        result = "".join(programs)
        positions_seen[i] = result
        if result == "abcdefghijklmnop":
            break
    remainder = 1_000_000_000 % i
    print(positions_seen[remainder])
