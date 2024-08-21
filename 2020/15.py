with open("./2020/resources/15.txt") as f:
    starting_numbers = [int(x) for x in f.read().strip().split(",")]


def get_number_said(n: int) -> int:
    lookup: dict[int, tuple[int | None, int]] = {num: (None, i) for i, num in enumerate(starting_numbers, start=1)}
    last_spoken = starting_numbers[-1]
    for turn_number in range(len(starting_numbers) + 1, n + 1):
        if last_spoken not in lookup:
            number_to_say = 0
        else:
            interval = lookup[last_spoken]
            if interval[0] is None:
                number_to_say = 0
            else:
                number_to_say = interval[1] - interval[0]
        if number_to_say not in lookup:
            lookup[number_to_say] = (None, turn_number)
        else:
            lookup[number_to_say] = (lookup[number_to_say][1], turn_number)
        last_spoken = number_to_say
    return last_spoken


def problem_1() -> None:
    print(get_number_said(2020))


def problem_2() -> None:
    print(get_number_said(30000000))
