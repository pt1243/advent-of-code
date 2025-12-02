from io import StringIO

from more_itertools import split_when

with open("./2015/resources/10.txt") as f:
    starting_sequence = f.read().strip()


def look_and_say(steps: int) -> int:
    current_sequence = starting_sequence
    for _ in range(steps):
        new_sequence = StringIO()
        for same_digits in split_when(current_sequence, lambda x, y: x != y):  # faster than itertools.groupby
            new_sequence.write(str(len(same_digits)))
            new_sequence.write(same_digits[0])
        current_sequence = new_sequence.getvalue()
    return len(current_sequence)


def problem_1() -> None:
    print(look_and_say(40))


def problem_2() -> None:
    print(look_and_say(50))
