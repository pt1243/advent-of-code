with open("./2015/resources/2.txt") as f:
    boxes = f.read().splitlines()


def part_1() -> None:
    total = 0
    for line in boxes:
        length, width, height = (int(i) for i in line.split("x"))
        lw = length * width
        lh = length * height
        wh = width * height
        total += 2 * lw + 2 * lh + 2 * wh
        total += min(lw, lh, wh)
    print(total)


def part_2() -> None:
    total = 0
    for line in boxes:
        length, width, height = (int(i) for i in line.split("x"))
        perimeter_lw = 2 * length + 2 * width
        perimeter_lh = 2 * length + 2 * height
        perimeter_wh = 2 * width + 2 * height
        total += min(perimeter_lw, perimeter_lh, perimeter_wh)
        total += length * width * height
    print(total)
