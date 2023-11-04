from math import sqrt, ceil


target = 34000000


def sum_divisors(n: int) -> set[int]:
    found: set[int] = set()
    for i in range(1, ceil(sqrt(n)) + 1):
        if n % i == 0:
            found.add(i)
            found.add(n // i)
    return sum(found)


def sum_divisors_part_2(n: int) -> set[int]:
    found: set[int] = set()
    for i in range(1, ceil(sqrt(n)) + 1):
        if n % i == 0:
            f1, f2 = i, n // i
            if f1 <= 50:
                found.add(f2)
            if f2 <= 50:
                found.add(f1)
    return sum(found)


def problem_1():
    n = 1
    while True:
        current_house_total = 10 * sum_divisors(n)
        if current_house_total >= target:
            print(n)
            break
        n += 1


def problem_2():
    n = 1
    while True:
        current_house_total = 11 * sum_divisors_part_2(n)
        if current_house_total >= target:
            print(n)
            break
        n += 1
