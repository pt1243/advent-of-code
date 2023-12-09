with open('./2023/resources/9.txt') as f:
    lines = [[int(c) for c in line.strip().split()] for line in f]


def problem_1() -> None:
    sum_extrapolated_values = 0
    for line in lines:
        all_differences = [line]
        last_line = all_differences[-1]
        while not all(c == 0 for c in last_line):
            new_line: list[int] = []
            for c1, c2 in zip(last_line[:-1], last_line[1:]):
                new_line.append(c2 - c1)
            all_differences.append(new_line)
            last_line = new_line
        for i, diff_line in enumerate(reversed(all_differences)):
            if i == 0:
                diff_line.append(0)
                continue
            diff_line.append(diff_line[-1] + all_differences[len(all_differences) - i][-1])
        sum_extrapolated_values += all_differences[0][-1]
    print(sum_extrapolated_values)


def problem_2() -> None:
    sum_extrapolated_values = 0
    for line in lines:
        all_differences = [line]
        last_line = all_differences[-1]
        while not all(c == 0 for c in last_line):
            new_line: list[int] = []
            for c1, c2 in zip(last_line[:-1], last_line[1:]):
                new_line.append(c2 - c1)
            all_differences.append(new_line)
            last_line = new_line
        for i, diff_line in enumerate(reversed(all_differences)):
            if i == 0:
                diff_line.append(0)
                continue
            diff_line.insert(0, diff_line[0] - all_differences[len(all_differences) - i][0])
        sum_extrapolated_values += all_differences[0][0]
    print(sum_extrapolated_values)
