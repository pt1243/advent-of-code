with open("./2022/resources/5.txt") as f:
    text = f.read().rstrip()


def part_1() -> None:
    starting_stacks, moves = text.split("\n\n")
    lines = starting_stacks.split("\n")[:-1]
    num_stacks = max(len(line) for line in lines) // 4 + 1
    stacks: list[list[str]] = [[] for _ in range(num_stacks)]
    for line in reversed(lines):
        for i, char in enumerate(line[1::4]):
            if char != " ":
                stacks[i].append(char)

    for line in moves.split("\n"):
        num, source, destination = (int(x) for x in line.split()[1::2])
        for _ in range(num):
            stacks[destination - 1].append(stacks[source - 1].pop())
    print("".join(stack[-1] for stack in stacks))


def part_2() -> None:
    starting_stacks, moves = text.split("\n\n")
    lines = starting_stacks.split("\n")[:-1]
    num_stacks = max(len(line) for line in lines) // 4 + 1
    stacks: list[list[str]] = [[] for _ in range(num_stacks)]
    for line in reversed(lines):
        for i, char in enumerate(line[1::4]):
            if char != " ":
                stacks[i].append(char)

    for line in moves.split("\n"):
        num, source, destination = (int(x) for x in line.split()[1::2])
        stacks[destination - 1].extend(stacks[source - 1][-num:])
        stacks[source - 1] = stacks[source - 1][:-num]
    print("".join(stack[-1] for stack in stacks))
