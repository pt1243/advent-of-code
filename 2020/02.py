from collections import Counter

with open("./2020/resources/2.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    num_valid = 0
    for line in lines:
        num_range, char, password = line.split()
        char = char[:-1]
        low, high = (int(x) for x in num_range.split("-"))
        if low <= Counter(password)[char] <= high:
            num_valid += 1
    print(num_valid)


def problem_2() -> None:
    num_valid = 0
    for line in lines:
        num_range, char, password = line.split()
        char = char[:-1]
        first_index, second_index = (int(x) for x in num_range.split("-"))
        if (password[first_index - 1] == char) + (password[second_index - 1] == char) == 1:
            num_valid += 1
    print(num_valid)
