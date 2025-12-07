from collections import defaultdict

with open("./2025/resources/7.txt") as f:
    lines = f.read().splitlines()


def part_1() -> None:
    start_col = lines[0].index("S")
    current_positions = {start_col}
    splits = 0
    for line in lines[1:]:
        new_positions: set[int] = set()
        for pos in current_positions:
            if line[pos] == "^":
                splits += 1
                new_positions.add(pos - 1)
                new_positions.add(pos + 1)
            else:
                new_positions.add(pos)
            current_positions = new_positions
    print(splits)


def part_2() -> None:
    start_col = lines[0].index("S")
    counts: defaultdict[int, int] = defaultdict(int)
    counts[start_col] = 1
    for line in lines[1:]:
        new_counts: defaultdict[int, int] = defaultdict(int)
        for pos, count in list(counts.items()):
            if line[pos] == "^":
                new_counts[pos - 1] += count
                new_counts[pos + 1] += count
            else:
                new_counts[pos] += count
        counts = new_counts
    print(sum(counts.values()))
