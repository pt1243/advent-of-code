with open("./2022/resources/1.txt") as f:
    text = f.read().strip()


def part_1() -> None:
    print(max((sum(int(line) for line in block.split("\n"))) for block in text.split("\n\n")))


def part_2() -> None:
    print(sum(sorted(((sum(int(line) for line in block.split("\n"))) for block in text.split("\n\n")))[-3:]))
