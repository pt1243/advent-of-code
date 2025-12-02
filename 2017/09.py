with open("./2017/resources/9.txt") as f:
    text = f.read().strip()


def part_1() -> None:
    depth = 0
    total_score = 0
    in_garbage = False
    i = 0
    while i < len(text):
        char = text[i]
        if char == "!":
            i += 2
        elif char == ">":
            in_garbage = False
            i += 1
        elif in_garbage:
            i += 1
        elif char == "<":
            i += 1
            in_garbage = True
        elif char == "{":
            depth += 1
            total_score += depth
            i += 1
        elif char == "}":
            depth -= 1
            i += 1
        else:
            i += 1
    print(total_score)


def part_2() -> None:
    in_garbage = False
    i = 0
    characters = 0
    while i < len(text):
        char = text[i]
        if char == "!":
            i += 2
        elif char == ">":
            in_garbage = False
            i += 1
        elif in_garbage:
            characters += 1
            i += 1
        elif char == "<":
            i += 1
            in_garbage = True
        else:
            i += 1
    print(characters)
