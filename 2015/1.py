with open('./2015/resources/1.txt') as f:
    input_string = f.read().strip()


def problem_1() -> None:
    floor = 0
    for char in input_string:
        if char == "(":
            floor += 1
        else:
            floor -= 1
    print(floor)


def problem_2() -> None:
    floor = 0
    for idx, char in enumerate(input_string):
        if char == "(":
            floor += 1
        else:
            floor -= 1
        if floor == -1:
            print(idx + 1)
            break
