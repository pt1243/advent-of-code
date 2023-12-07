from collections import deque


with open('./2017/resources/6.txt') as f:
    banks = deque(int(c) for c in f.read().strip().split())


def problem_1() -> None:
    num_banks = len(banks)
    seen: set[tuple[int, ...]] = {tuple(banks)}
    cycles = 0
    while True:
        max_idx = banks.index(max(banks))
        banks_to_redistribute = banks[max_idx]
        banks[max_idx] = 0
        shared, extra = divmod(banks_to_redistribute, num_banks)
        for i in range(num_banks):
            banks[i] += shared
        banks.rotate(-max_idx - 1)
        for i in range(extra):
            banks[i] += 1
        banks.rotate(max_idx + 1)
        cycles += 1
        tup = tuple(banks)
        if tup in seen:
            print(cycles)
            return
        seen.add(tuple(banks))


def problem_2() -> None:
    num_banks = len(banks)
    seen: list[tuple[int, ...]] = [tuple(banks)]
    cycles = 0
    while True:
        max_idx = banks.index(max(banks))
        banks_to_redistribute = banks[max_idx]
        banks[max_idx] = 0
        shared, extra = divmod(banks_to_redistribute, num_banks)
        for i in range(num_banks):
            banks[i] += shared
        banks.rotate(-max_idx - 1)
        for i in range(extra):
            banks[i] += 1
        banks.rotate(max_idx + 1)
        cycles += 1
        tup = tuple(banks)
        if tup in seen:
            print(cycles - seen.index(tup))
            return
        seen.append(tuple(banks))
