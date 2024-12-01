from collections import defaultdict


with open("./2024/resources/1.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    first_col: list[int] = []
    second_col: list[int] = []
    for line in lines:
        split = line.split()
        first_col.append(int(split[0]))
        second_col.append(int(split[1]))
    print(sum(abs(id_1 - id_2) for id_1, id_2 in zip(sorted(first_col), sorted(second_col))))


def problem_2() -> None:
    first_col: defaultdict[int, int] = defaultdict(int)
    second_col: defaultdict[int, int] = defaultdict(int)
    for line in lines:
        split = line.split()
        first_col[int(split[0])] += 1
        second_col[int(split[1])] += 1
    print(sum(num * times * second_col[num] for num, times in first_col.items()))
