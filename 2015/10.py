from more_itertools import split_when


with open("./2015/resources/10.txt") as f:
    val = f.read().strip()


def problem_1() -> None:
    current_val = val
    for _ in range(40):
        new_val = ""
        for same_digits in split_when(current_val, lambda x, y: x != y):
            new_val += str(len(same_digits))
            new_val += same_digits[0]
        current_val = new_val
    print(len(current_val))


def problem_2() -> None:
    current_val = val
    for _ in range(50):
        new_val = ""
        for same_digits in split_when(current_val, lambda x, y: x != y):
            new_val += str(len(same_digits))
            new_val += same_digits[0]
        current_val = new_val
    print(len(current_val))
