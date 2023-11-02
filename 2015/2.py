def problem_1():
    with open("./2015/resources/2.txt") as f:
        boxes = [line.strip() for line in f]
    total = 0
    for line in boxes:
        l, w, h = (int(i) for i in line.split('x'))
        lw = l * w
        lh = l * h
        wh = w * h
        total += 2*lw + 2*lh + 2*wh
        total += min(lw, lh, wh)
    print(total)


def problem_2():
    with open("./2015/resources/2.txt") as f:
        boxes = [line.strip() for line in f]
    total = 0
    for line in boxes:
        l, w, h = (int(i) for i in line.split('x'))
        perimeter_lw = 2*l + 2*w
        perimeter_lh = 2*l + 2*h
        perimeter_wh = 2*w + 2*h
        total += min(perimeter_lw, perimeter_lh, perimeter_wh)
        total += l * w * h
    print(total)
