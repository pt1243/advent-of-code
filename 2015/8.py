with open('./2015/resources/8.txt') as f:
    strings = [line.strip() for line in f]


def problem_1():
    total = sum(len(s) - len(eval(s)) for s in strings)
    print(total)


def problem_2():
    total = sum(2 + s.count("\\") + s.count("\"") for s in strings)
    print(total)
