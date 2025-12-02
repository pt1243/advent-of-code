from collections import defaultdict
from itertools import combinations, count
from math import gcd

with open("./2024/resources/8.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    height, width = len(lines), len(lines[0])
    antennas: defaultdict[str, list[tuple[int, int]]] = defaultdict(list)
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char != ".":
                antennas[char].append((row, col))

    antinode_positions: set[tuple[int, int]] = set()
    for positions in antennas.values():
        for antenna_1, antenna_2 in combinations(positions, 2):
            drow = antenna_2[0] - antenna_1[0]
            dcol = antenna_2[1] - antenna_1[1]
            antinode_1 = (antenna_1[0] - drow, antenna_1[1] - dcol)
            antinode_2 = (antenna_2[0] + drow, antenna_2[1] + dcol)
            antinode_positions.add(antinode_1)
            antinode_positions.add(antinode_2)
    print(sum(1 for antinode in antinode_positions if 0 <= antinode[0] < width and 0 <= antinode[1] < height))


def problem_2() -> None:
    height, width = len(lines), len(lines[0])
    antennas: defaultdict[str, list[tuple[int, int]]] = defaultdict(list)
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char != ".":
                antennas[char].append((row, col))

    antinode_positions: set[tuple[int, int]] = set()
    for positions in antennas.values():
        for antenna_1, antenna_2 in combinations(positions, 2):
            drow = antenna_2[0] - antenna_1[0]
            dcol = antenna_2[1] - antenna_1[1]
            row_step = drow // gcd(abs(drow), abs(dcol))
            col_step = dcol // gcd(abs(drow), abs(dcol))
            for i in count(1):
                antinode = (antenna_1[0] - i * row_step, antenna_1[1] - i * col_step)
                if not 0 <= antinode[0] < height or not 0 <= antinode[1] < width:
                    break
                antinode_positions.add(antinode)
            for i in count():
                antinode = (antenna_1[0] + i * row_step, antenna_1[1] + i * col_step)
                if not 0 <= antinode[0] < height or not 0 <= antinode[1] < width:
                    break
                antinode_positions.add(antinode)
    print(len(antinode_positions))
