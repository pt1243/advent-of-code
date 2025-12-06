from functools import reduce
from operator import add, mul

with open("./2025/resources/6.txt") as f:
    lines = f.read().splitlines()


def part_1() -> None:
    total = 0
    problems: list[list[str]] = [[] for _ in range(len(lines[0].split()))]
    for line in lines:
        for problem, item in zip(problems, line.split()):
            problem.append(item)

    operators = {"+": add, "*": mul}
    for problem in problems:
        total += reduce(operators[problem[-1]], map(int, problem[:-1]))
    print(total)


def part_2() -> None:
    total = 0
    problems: list[list[str]] = [[] for _ in range(len(lines[0].split()))]
    for line in lines:
        for problem, item in zip(problems, line.split()):
            problem.append(item)

    maximum_number_lengths = [max(len(item) for item in col[:-1]) for col in problems]

    ops = {"+": add, "*": mul}
    problem_start_index = 0
    for problem, maximum_number_length in zip(problems, maximum_number_lengths):
        vals = [
            int("".join(line[i + problem_start_index] for line in lines[:-1] if line[i + problem_start_index] != " "))
            for i in range(maximum_number_length)
        ]
        problem_start_index += maximum_number_length + 1
        total += reduce(ops[problem[-1]], vals)
    print(total)
