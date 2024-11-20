with open("./2021/resources/13.txt") as f:
    text = f.read().strip()


def problem_1() -> None:
    dots, folds = text.split("\n\n")
    current_dots = {(int(line.split(",")[0]), int(line.split(",")[1])) for line in dots.split("\n")}
    fold = folds.split("\n")[0]
    direction, value_str = fold.split()[-1].split("=")
    value = int(value_str)
    if direction == "y":
        new_dots = {(dot[0], dot[1] if dot[1] < value else value - (dot[1] - value)) for dot in current_dots}
    else:
        new_dots = {(dot[0] if dot[0] < value else value - (dot[0] - value), dot[1]) for dot in current_dots}
    print(len(new_dots))


def problem_2() -> None:
    dots, folds = text.split("\n\n")
    current_dots = {(int(line.split(",")[0]), int(line.split(",")[1])) for line in dots.split("\n")}
    for fold in folds.split("\n"):
        direction, value_str = fold.split()[-1].split("=")
        value = int(value_str)
        if direction == "y":
            new_dots = {(dot[0], dot[1] if dot[1] < value else value - (dot[1] - value)) for dot in current_dots}
        else:
            new_dots = {(dot[0] if dot[0] < value else value - (dot[0] - value), dot[1]) for dot in current_dots}
        current_dots = new_dots
    min_x = min(dot[0] for dot in current_dots)
    max_x = max(dot[0] for dot in current_dots)
    min_y = min(dot[1] for dot in current_dots)
    max_y = max(dot[1] for dot in current_dots)
    print(
        "\n".join(
            "".join("█" if (x, y) in current_dots else " " for x in range(min_x, max_x + 1))
            for y in range(min_y, max_y + 1)
        )
    )
