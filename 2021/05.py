from collections import defaultdict

with open("./2021/resources/5.txt") as f:
    lines = f.read().splitlines()


def part_1() -> None:
    counts: defaultdict[tuple[int, int], int] = defaultdict(int)
    for line in lines:
        start, end = line.split(" -> ")
        x1, y1 = (int(val) for val in start.split(","))
        x2, y2 = (int(val) for val in end.split(","))
        if not (x1 == x2 or y1 == y2):
            continue
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                counts[x1, y] += 1
        else:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                counts[x, y1] += 1
    print(sum(1 for count in counts.values() if count >= 2))


def part_2() -> None:
    counts: defaultdict[tuple[int, int], int] = defaultdict(int)
    for line in lines:
        start, end = line.split(" -> ")
        x1, y1 = (int(val) for val in start.split(","))
        x2, y2 = (int(val) for val in end.split(","))
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                counts[x1, y] += 1
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                counts[x, y1] += 1
        else:
            x_step = 1 if x2 >= x1 else -1
            y_step = 1 if y2 >= y1 else -1
            for i in range(abs(x2 - x1) + 1):
                counts[x1 + x_step * i, y1 + y_step * i] += 1
    print(sum(1 for count in counts.values() if count >= 2))
