from more_itertools import sliding_window

with open("./2024/resources/4.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    total = 0
    for row in lines:
        for chars in sliding_window(row, 4):
            if "".join(chars) in {"XMAS", "SAMX"}:
                total += 1
    for col in zip(*lines):
        for chars in sliding_window(col, 4):
            if "".join(chars) in {"XMAS", "SAMX"}:
                total += 1
    right_shifted_lines = [i * "_" + line + (len(line) - i) * "_" for i, line in enumerate(lines)]
    for col in zip(*right_shifted_lines):
        for chars in sliding_window(col, 4):
            if "".join(chars) in {"XMAS", "SAMX"}:
                total += 1
    left_shifted_lines = [(len(line) - i) * "_" + line + i * "_" for i, line in enumerate(lines)]
    for col in zip(*left_shifted_lines):
        for chars in sliding_window(col, 4):
            if "".join(chars) in {"XMAS", "SAMX"}:
                total += 1
    print(total)


def problem_2() -> None:
    total = 0
    for line_batch in sliding_window(lines, 3):
        for col_1, col_2, col_3 in sliding_window(zip(*line_batch), 3):
            if (
                col_2[1] == "A"
                and ((col_1[0] == "M" and col_3[2] == "S") or (col_1[0] == "S" and col_3[2] == "M"))
                and ((col_1[2] == "M" and col_3[0] == "S") or (col_1[2] == "S" and col_3[0] == "M"))
            ):
                total += 1
    print(total)
