with open('./2017/resources/1.txt') as f:
    num = f.read().strip()


def problem_1() -> None:
    total = 0
    for c1, c2 in zip(num, num[1:] + num[0]):
        if c1 == c2:
            total += int(c1)
    print(total)


def problem_2() -> None:
    total = 0
    num_ahead = len(num) // 2
    for c1, c2 in zip(num, num[num_ahead:] + num[:num_ahead]):
        if c1 == c2:
            total += int(c1)
    print(total)
