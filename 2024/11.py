from collections import defaultdict
from collections.abc import Iterable

with open("./2024/resources/11.txt") as f:
    starting_stones = f.read().strip().split()


def run_stones(starting_stones: Iterable[str], blinks: int) -> int:
    stones: defaultdict[str, int] = defaultdict(int)
    for stone in starting_stones:
        stones[stone] += 1

    for _ in range(blinks):
        new_stones: defaultdict[str, int] = defaultdict(int)
        num_zeros = stones.pop("0", 0)
        if num_zeros:
            new_stones["1"] = num_zeros
        for number, count in stones.items():
            if len(number) % 2 == 0:
                left = number[: len(number) // 2]
                right = number[len(number) // 2 :]
                new_stones[left.lstrip("0").zfill(1)] += count
                new_stones[right.lstrip("0").zfill(1)] += count
            else:
                new_stones[str(int(number) * 2024)] += count
        stones = new_stones
    return sum(stones.values())


def part_1() -> None:
    print(run_stones(starting_stones, 25))


def part_2() -> None:
    print(run_stones(starting_stones, 75))
