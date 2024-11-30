from itertools import count
from math import isqrt


with open("./2015/resources/20.txt") as f:
    target = int(f.read().strip())


def sum_divisors(n: int) -> int:
    found: set[int] = set()
    for i in range(1, isqrt(n) + 2):
        if n % i == 0:
            found.add(i)
            found.add(n // i)
    return sum(found)


def sum_divisors_part_2(n: int) -> int:
    found: set[int] = set()
    for i in range(1, isqrt(n) + 2):
        if n % i == 0:
            f1, f2 = i, n // i
            if f1 <= 50:
                found.add(f2)
            if f2 <= 50:
                found.add(f1)
    return sum(found)


def problem_1() -> None:
    for n in count(1):
        current_house_total = 10 * sum_divisors(n)
        if current_house_total >= target:
            print(n)
            break


def problem_2() -> None:
    for n in count(1):
        current_house_total = 11 * sum_divisors_part_2(n)
        if current_house_total >= target:
            print(n)
            break
