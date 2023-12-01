from more_itertools import split_when


def problem_1() -> None:
    val = "1113122113"
    for _ in range(40):
        new_val = ""
        for same_digits in split_when(val, lambda x, y: x != y):
            new_val += str(len(same_digits))
            new_val += same_digits[0]
        val = new_val
    print(len(val))


def problem_2() -> None:
    val = "1113122113"
    for _ in range(50):
        new_val = ""
        for same_digits in split_when(val, lambda x, y: x != y):
            new_val += str(len(same_digits))
            new_val += same_digits[0]
        val = new_val
    print(len(val))
