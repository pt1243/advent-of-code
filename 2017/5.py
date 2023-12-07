with open('./2017/resources/5.txt') as f:
    jumps = [int(line.strip()) for line in f]


def problem_1() -> None:
    i = 0
    steps = 0
    while 0 <= i < len(jumps):
        current = jumps[i]
        jumps[i] += 1
        i += current
        steps += 1
    print(steps)


def problem_2() -> None:
    i = 0
    steps = 0
    while 0 <= i < len(jumps):
        current = jumps[i]
        jumps[i] += -1 if current >= 3 else 1
        i += current
        steps += 1
    print(steps)
