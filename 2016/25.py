from itertools import count

with open("./2016/resources/25.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    constant_1 = int(lines[1].split()[1])
    constant_2 = int(lines[2].split()[1])
    for i in count(1):
        output = []
        a = i + constant_1 * constant_2
        while a != 0:
            b = a
            c = 2 if b % 2 == 0 else 1
            a = b // 2
            b = 2 - c
            output.append(b)
        if len(output) % 2 == 0:
            zero_list = [0 for _ in range(len(output) // 2)]
            one_list = [1 for _ in range(len(output) // 2)]
            if output[::2] == zero_list and output[1::2] == one_list:
                print(i)
                return
