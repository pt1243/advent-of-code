import re


with open("./2020/resources/24.txt") as f:
    lines = f.read().splitlines()


def perform_renovations() -> set[tuple[int, int]]:
    black_tiles: set[tuple[int, int]] = set()
    directions = {
        "w": (-1, 0),
        "nw": (0, -1),
        "sw": (-1, 1),
        "e": (1, 0),
        "ne": (1, -1),
        "se": (0, 1),
    }

    pattern = re.compile(r"(e|se|sw|w|nw|ne)")
    for line in lines:
        q, r = 0, 0
        for move in re.findall(pattern, line):
            dq, dr = directions[move]
            q += dq
            r += dr
        if (q, r) in black_tiles:
            black_tiles.remove((q, r))
        else:
            black_tiles.add((q, r))

    return black_tiles


def problem_1() -> None:
    black_tiles = perform_renovations()
    print(len(black_tiles))


def problem_2() -> None:
    current_black_tiles = perform_renovations()

    for _ in range(100):
        tiles_to_consider = current_black_tiles.copy()
        for q, r in current_black_tiles:
            tiles_to_consider.update({(q - 1, r), (q, r - 1), (q - 1, r + 1), (q + 1, r), (q + 1, r - 1), (q, r + 1)})

        new_black_tiles: set[tuple[int, int]] = set()
        for q, r in tiles_to_consider:
            num_black_neighbours = (
                ((q - 1, r) in current_black_tiles)
                + ((q, r - 1) in current_black_tiles)
                + ((q - 1, r + 1) in current_black_tiles)
                + ((q + 1, r) in current_black_tiles)
                + ((q + 1, r - 1) in current_black_tiles)
                + ((q, r + 1) in current_black_tiles)
            )
            if (q, r) in current_black_tiles and not (num_black_neighbours == 0 or num_black_neighbours > 2):
                new_black_tiles.add((q, r))
            if (q, r) not in current_black_tiles and num_black_neighbours == 2:
                new_black_tiles.add((q, r))

        current_black_tiles = new_black_tiles
    print(len(current_black_tiles))
