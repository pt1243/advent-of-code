from itertools import batched


with open("./2022/resources/10.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    sum_of_signal_strengths = 0
    x_register = 1
    cycle = 1
    for line in lines:
        if cycle % 40 == 20:
            sum_of_signal_strengths += cycle * x_register
            if cycle == 220:
                break
        if line.startswith("noop"):
            cycle += 1
        else:
            cycle += 1
            if cycle % 40 == 20:
                sum_of_signal_strengths += cycle * x_register
                if cycle == 220:
                    break
            value = int(line.split()[1])
            x_register += value
            cycle += 1
    print(sum_of_signal_strengths)


def problem_2() -> None:
    sprite_middle = 1
    cycle = 0
    pixels: list[bool] = []
    for line in lines:
        pixel_col = cycle % 40
        pixels.append(pixel_col in {sprite_middle - 1, sprite_middle, sprite_middle + 1})
        if line.startswith("noop"):
            cycle += 1
        else:
            cycle += 1
            pixel_col = cycle % 40
            pixels.append(pixel_col in {sprite_middle - 1, sprite_middle, sprite_middle + 1})
            value = int(line.split()[1])
            sprite_middle += value
            cycle += 1
    print("\n".join("".join("█" if char else " " for char in row) for row in batched(pixels, 40)))
