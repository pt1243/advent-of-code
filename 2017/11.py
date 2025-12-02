with open("./2017/resources/11.txt") as f:
    moves = f.read().strip().split(",")


# https://www.redblobgames.com/grids/hexagons/#distances
directions = {
    "n": (0, -1),
    "nw": (-1, 0),
    "ne": (1, -1),
    "s": (0, 1),
    "sw": (-1, 1),
    "se": (1, 0),
}


def part_1() -> None:
    q, r = 0, 0
    for move in moves:
        dq, dr = directions[move]
        q += dq
        r += dr
    s = -q - r
    print(max(abs(q), abs(r), abs(s)))


def part_2() -> None:
    q, r = 0, 0
    max_dist = 0
    for move in moves:
        dq, dr = directions[move]
        q += dq
        r += dr
        s = -q - r
        dist = max(abs(q), abs(r), abs(s))
        max_dist = max(dist, max_dist)
    print(max_dist)
