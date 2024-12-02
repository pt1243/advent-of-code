from itertools import batched


with open("./2016/resources/3.txt") as f:
    triangles = f.read().splitlines()


def problem_1() -> None:
    count = 0
    for triangle in triangles:
        a, b, c = (int(side) for side in triangle.split())
        if a + b > c and a + c > b and b + c > a:
            count += 1
    print(count)


def problem_2() -> None:
    count = 0
    for row_1, row_2, row_3 in batched(triangles, 3):
        a1, a2, a3 = (int(side) for side in row_1.split())
        b1, b2, b3 = (int(side) for side in row_2.split())
        c1, c2, c3 = (int(side) for side in row_3.split())

        if a1 + b1 > c1 and a1 + c1 > b1 and b1 + c1 > a1:
            count += 1
        if a2 + b2 > c2 and a2 + c2 > b2 and b2 + c2 > a2:
            count += 1
        if a3 + b3 > c3 and a3 + c3 > b3 and b3 + c3 > a3:
            count += 1
    print(count)
