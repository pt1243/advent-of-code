from itertools import count

with open("./2017/resources/13.txt") as f:
    layers = {int(line.split(": ")[0]): int(line.split(": ")[1]) for line in f.read().splitlines()}


def get_position(length: int, steps: int) -> int:
    full_length = length * 2 - 2
    pos = steps % full_length
    if pos >= length:
        extra = pos - length
        pos = length - 2 - extra
    return pos


def problem_1() -> None:
    severity = 0
    max_depth = max(layers)
    for current_position in range(max_depth + 1):
        if current_position in layers:
            if get_position(layers[current_position], current_position) == 0:
                severity += current_position * layers[current_position]
    print(severity)


def problem_2() -> None:
    max_depth = max(layers)
    for start_offset in count():
        for current_position in range(max_depth + 1):
            if current_position in layers:
                if get_position(layers[current_position], current_position + start_offset) == 0:
                    break
        else:
            print(start_offset)
            break
