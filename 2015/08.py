import ast


with open("./2015/resources/8.txt") as f:
    strings = f.read().splitlines()


def problem_1() -> None:
    print(sum(len(s) - len(ast.literal_eval(s)) for s in strings))


def problem_2() -> None:
    print(sum(2 + s.count("\\") + s.count('"') for s in strings))
