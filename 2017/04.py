with open("./2017/resources/4.txt") as f:
    lines = f.read().splitlines()


def part_1() -> None:
    total_valid = 0
    for line in lines:
        words = line.split()
        if len(words) == len(set(words)):
            total_valid += 1
    print(total_valid)


def part_2() -> None:
    total_valid = 0
    for line in lines:
        words_letters_sorted = ["".join(sorted(word)) for word in line.split()]
        if len(words_letters_sorted) == len(set(words_letters_sorted)):
            total_valid += 1
    print(total_valid)
