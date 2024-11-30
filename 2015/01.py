with open("./2015/resources/1.txt") as f:
    input_string = f.read().strip()


def problem_1() -> None:
    print(sum(1 if char == "(" else -1 for char in input_string))


def problem_2() -> None:
    floor = 0
    for idx, char in enumerate(input_string, start=1):
        floor += 1 if char == "(" else -1
        if floor == -1:
            print(idx)
            break
