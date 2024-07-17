from collections import Counter
from itertools import combinations


with open("./2018/resources/2.txt") as f:
    lines = [line.strip() for line in f]


def problem_1() -> None:
    two, three = 0, 0
    for box_id in lines:
        c = Counter(box_id)
        if 2 in c.values():
            two += 1
        if 3 in c.values():
            three += 1
    print(two * three)


def problem_2() -> None:
    for box_1, box_2 in combinations(lines, 2):
        different_letters = 0
        for char_1, char_2 in zip(box_1, box_2):
            if char_1 != char_2:
                different_letters += 1
                if different_letters > 1:
                    break
        if different_letters == 1:
            print("".join(char_1 for char_1, char_2 in zip(box_1, box_2) if char_1 == char_2))
            return
