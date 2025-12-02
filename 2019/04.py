from itertools import groupby, pairwise

with open("./2019/resources/4.txt") as f:
    low, high = (int(val) for val in f.read().strip().split("-"))


def problem_1() -> None:
    num_meeting_criteria = 0
    for password in range(low, high + 1):
        digits = str(password)
        if any(d1 == d2 for d1, d2 in pairwise(digits)) and all(d1 <= d2 for d1, d2 in pairwise(digits)):
            num_meeting_criteria += 1
    print(num_meeting_criteria)


def problem_2() -> None:
    num_meeting_criteria = 0
    for password in range(low, high + 1):
        digits = str(password)
        if all(d1 <= d2 for d1, d2 in pairwise(digits)) and any(len(list(g)) == 2 for _, g in groupby(digits)):
            num_meeting_criteria += 1
    print(num_meeting_criteria)
