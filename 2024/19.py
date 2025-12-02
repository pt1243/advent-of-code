from functools import cache

with open("./2024/resources/19.txt") as f:
    text = f.read().strip()


@cache
def num_ways(target: str, options: tuple[str, ...]) -> int:
    if not target:
        return 1
    total = 0
    for option in options:
        if target.startswith(option):
            total += num_ways(target[len(option) :], options)
    return total


def problem_1() -> None:
    options_text, targets = text.split("\n\n")
    options = tuple(options_text.split(", "))
    print(sum(1 for target in targets.split("\n") if num_ways(target, options)))


def problem_2() -> None:
    options_text, targets = text.split("\n\n")
    options = tuple(options_text.split(", "))
    print(sum(num_ways(target, options) for target in targets.split("\n")))
