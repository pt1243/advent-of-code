with open("./2020/resources/8.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    accumulator = 0
    seen: set[int] = set()
    i = 0
    while i not in seen:
        seen.add(i)
        operation = lines[i].split()[0]
        argument = int(lines[i].split()[1])
        if operation == "acc":
            accumulator += argument
            i += 1
        elif operation == "jmp":
            i += argument
        else:
            i += 1
    print(accumulator)


def problem_2() -> None:
    for instruction_to_change in range(len(lines)):
        seen: set[int] = set()
        accumulator = 0
        i = 0
        while i not in seen:
            if not 0 <= i < len(lines):
                print(accumulator)
                return
            seen.add(i)
            operation = lines[i].split()[0]
            argument = int(lines[i].split()[1])
            if i == instruction_to_change:
                if operation == "jmp":
                    operation = "nop"
                elif operation == "nop":
                    operation = "jmp"
            if operation == "acc":
                accumulator += argument
                i += 1
            elif operation == "jmp":
                i += argument
            else:
                i += 1
