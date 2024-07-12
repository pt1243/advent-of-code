from collections import deque


n_times = 354


def spinlock(n: int, iterations: int) -> deque[int]:
    lst = deque([0])
    for i in range(1, iterations + 1):
        lst.rotate(-n)
        lst.append(i)
    return lst


def problem_1() -> None:
    result = spinlock(n_times, 2017)
    print(result[0])


def problem_2() -> None:
    result = spinlock(n_times, 50_000_000)
    print(result[result.index(0) + 1])
