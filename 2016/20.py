from itertools import count


with open('./2016/resources/20.txt') as f:
    lines = [line.strip() for line in f]
    for line in lines:
        lower, upper = line.split("-")


def problem_1() -> None:
    ranges = tuple(sorted(tuple(int(val) for val in line.split("-")) for line in lines))
    for i in count():
        if not any(lower <= i <= upper for lower, upper in ranges):
            print(i)
            break


def problem_2() -> None:
    total += 1
    ranges = tuple(sorted(tuple(int(val) for val in line.split("-")) for line in lines))
    for i in range(0, 4294967295 + 1):
        if not any(lower <= i <= upper for lower, upper in ranges):
            total += 1
    print(total)
