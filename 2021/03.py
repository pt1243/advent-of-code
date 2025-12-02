from collections import Counter

with open("./2021/resources/3.txt") as f:
    lines = f.read().splitlines()


def part_1() -> None:
    column_counters: list[Counter[str]] = [Counter() for _ in lines[0]]
    for line in lines:
        for c, char in zip(column_counters, line):
            c.update(char)
    gamma_rate = int("".join(c.most_common(1)[0][0] for c in column_counters), 2)
    epsilon_rate = int("".join(c.most_common()[-1][0] for c in column_counters), 2)
    print(gamma_rate * epsilon_rate)


def part_2() -> None:
    position = 0
    lines_to_keep = lines.copy()
    while True:
        most, least = Counter(line[position] for line in lines_to_keep).most_common()
        value_to_keep = "1" if most[1] == least[1] else most[0]
        lines_to_keep = [line for line in lines_to_keep if line[position] == value_to_keep]
        if len(lines_to_keep) == 1:
            oxygen_generator_rating = int(lines_to_keep[0], 2)
            break
        position += 1
    position = 0
    lines_to_keep = lines.copy()
    while True:
        most, least = Counter(line[position] for line in lines_to_keep).most_common()
        value_to_keep = "0" if most[1] == least[1] else least[0]
        lines_to_keep = [line for line in lines_to_keep if line[position] == value_to_keep]
        if len(lines_to_keep) == 1:
            co2_scrubber_rating = int(lines_to_keep[0], 2)
            break
        position += 1
    print(oxygen_generator_rating * co2_scrubber_rating)
