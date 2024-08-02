with open("./2023/resources/1.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    total = 0
    for line in lines:
        numbers: list[str] = []
        for char in line:
            if char.isnumeric():
                numbers.append(char)
        total += int(numbers[0] + numbers[-1])
    print(total)


def problem_2() -> None:
    total = 0

    number_names = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    for line in lines:
        numbers: set[tuple[int, str]] = set()
        for number_name, number_value in number_names.items():
            if number_name in line:
                first_idx = line.find(number_name)
                last_idx = line.rfind(number_name)
                numbers.add((first_idx, number_value))
                numbers.add((last_idx, number_value))
        for idx, char in enumerate(line):
            if char.isnumeric():
                numbers.add((idx, char))
        sorted_numbers = sorted(numbers)
        total += int(sorted_numbers[0][1] + sorted_numbers[-1][1])
    print(total)
