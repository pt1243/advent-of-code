with open("./2020/resources/6.txt") as f:
    text = f.read().strip()


def part_1() -> None:
    sum_of_counts = 0
    for group in text.split("\n\n"):
        group = group.replace("\n", "")
        sum_of_counts += len(set(group))
    print(sum_of_counts)


def part_2() -> None:
    sum_of_counts = 0
    for group in text.split("\n\n"):
        people = [set(line) for line in group.split()]
        sum_of_counts += len(people[0].intersection(*people[1:]))
    print(sum_of_counts)
