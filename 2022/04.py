with open("./2022/resources/4.txt") as f:
    lines = f.read().splitlines()


def part_1() -> None:
    total = 0
    for line in lines:
        first, second = line.split(",")
        first_lower, first_upper = (int(x) for x in first.split("-"))
        second_lower, second_upper = (int(x) for x in second.split("-"))
        if (first_lower <= second_lower and first_upper >= second_upper) or (
            second_lower <= first_lower and second_upper >= first_upper
        ):
            total += 1
    print(total)


def part_2() -> None:
    total = 0
    for line in lines:
        first, second = line.split(",")
        first_lower, first_upper = (int(x) for x in first.split("-"))
        second_lower, second_upper = (int(x) for x in second.split("-"))
        if (
            (second_lower <= first_lower <= second_upper)
            or (second_lower <= first_upper <= second_upper)
            or (first_lower <= second_lower <= first_upper)
            or (first_lower <= second_upper <= first_upper)
        ):
            total += 1
    print(total)
