with open("./2021/resources/11.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    width = len(lines[0])
    height = len(lines)
    total_flashes = 0
    current_brightnesses = {(row, col): int(char) for row, line in enumerate(lines) for col, char in enumerate(line)}
    for _ in range(100):
        flashed: set[tuple[int, int]] = set()
        new_brightnesses = {pos: brightness + 1 for pos, brightness in current_brightnesses.items()}
        while any(brightness > 9 for brightness in new_brightnesses.values()):
            for (row, col), brightness in new_brightnesses.copy().items():
                if brightness <= 9:
                    continue
                flashed.add((row, col))
                total_flashes += 1
                if row > 0:
                    if col > 0 and (row - 1, col - 1) not in flashed:
                        new_brightnesses[row - 1, col - 1] += 1
                    if (row - 1, col) not in flashed:
                        new_brightnesses[row - 1, col] += 1
                    if col < width - 1 and (row - 1, col + 1) not in flashed:
                        new_brightnesses[row - 1, col + 1] += 1
                if col > 0 and (row, col - 1) not in flashed:
                    new_brightnesses[row, col - 1] += 1
                if col < width - 1 and (row, col + 1) not in flashed:
                    new_brightnesses[row, col + 1] += 1
                if row < height - 1:
                    if col > 0 and (row + 1, col - 1) not in flashed:
                        new_brightnesses[row + 1, col - 1] += 1
                    if (row + 1, col) not in flashed:
                        new_brightnesses[row + 1, col] += 1
                    if col < width - 1 and (row + 1, col + 1) not in flashed:
                        new_brightnesses[row + 1, col + 1] += 1
                new_brightnesses[row, col] = 0
        current_brightnesses = new_brightnesses
    print(total_flashes)


def problem_2() -> None:
    width = len(lines[0])
    height = len(lines)
    current_brightnesses = {(row, col): int(char) for row, line in enumerate(lines) for col, char in enumerate(line)}
    step = 0
    while True:
        step += 1
        flashed: set[tuple[int, int]] = set()
        new_brightnesses = {pos: brightness + 1 for pos, brightness in current_brightnesses.items()}
        while any(brightness > 9 for brightness in new_brightnesses.values()):
            for (row, col), brightness in new_brightnesses.copy().items():
                if brightness <= 9:
                    continue
                flashed.add((row, col))
                if row > 0:
                    if col > 0 and (row - 1, col - 1) not in flashed:
                        new_brightnesses[row - 1, col - 1] += 1
                    if (row - 1, col) not in flashed:
                        new_brightnesses[row - 1, col] += 1
                    if col < width - 1 and (row - 1, col + 1) not in flashed:
                        new_brightnesses[row - 1, col + 1] += 1
                if col > 0 and (row, col - 1) not in flashed:
                    new_brightnesses[row, col - 1] += 1
                if col < width - 1 and (row, col + 1) not in flashed:
                    new_brightnesses[row, col + 1] += 1
                if row < height - 1:
                    if col > 0 and (row + 1, col - 1) not in flashed:
                        new_brightnesses[row + 1, col - 1] += 1
                    if (row + 1, col) not in flashed:
                        new_brightnesses[row + 1, col] += 1
                    if col < width - 1 and (row + 1, col + 1) not in flashed:
                        new_brightnesses[row + 1, col + 1] += 1
                new_brightnesses[row, col] = 0
        if len(flashed) == width * height:
            print(step)
            break
        current_brightnesses = new_brightnesses
