from more_itertools import sliding_window

with open("./2022/resources/6.txt") as f:
    text = f.read().strip()


def problem_1() -> None:
    for i, chars in enumerate(sliding_window(text, 4), start=4):
        if len(set(chars)) == 4:
            print(i)
            return


def problem_2() -> None:
    for i, chars in enumerate(sliding_window(text, 14), start=14):
        if len(set(chars)) == 14:
            print(i)
            return
