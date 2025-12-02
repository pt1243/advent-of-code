from collections import deque
from itertools import permutations

with open("./2016/resources/21.txt") as f:
    lines = f.read().splitlines()


def scramble(d: deque[str]) -> str:
    for line in lines:
        split = line.split()
        if "swap" in line:
            if "position" in line:
                idx1, idx2 = int(split[2]), int(split[5])
                d[idx1], d[idx2] = d[idx2], d[idx1]
            else:
                x, y = split[2], split[5]
                d = deque(y if char == x else (x if char == y else char) for char in d)
        elif "rotate" in line:
            if "position" not in line:
                n_rotations = int(split[2])
                n_rotations *= -1 if split[1] == "left" else 1
                d.rotate(n_rotations)
            else:
                index = d.index(split[6])
                n_rotations = 1 + index + (1 if index >= 4 else 0)
                d.rotate(n_rotations)
        elif "reverse" in line:
            idx1, idx2 = int(split[2]), int(split[4])
            vals: list[str] = []
            for i in range(idx1, idx2 + 1):
                vals.append(d[i])
            for i, val in enumerate(reversed(vals), idx1):
                d[i] = val
        else:
            idx1, idx2 = int(split[2]), int(split[5])
            val = d[idx1]
            del d[idx1]
            d.insert(idx2, val)
    return "".join(d)


def part_1() -> None:
    print(scramble(deque("abcdefgh")))


def part_2() -> None:
    target = "fbgdceah"

    for p in permutations(target):
        if scramble(deque("".join(p))) == target:
            print("".join(p))
            break
