from collections.abc import Generator
from itertools import accumulate, islice, pairwise, product

from more_itertools import sliding_window

with open("./2024/resources/22.txt") as f:
    secret_nums = [int(line) for line in f.read().splitlines()]


def calculate_secret_numbers(secret_num: int) -> Generator[int, None, None]:
    while True:
        yield secret_num
        secret_num = ((secret_num * 64) ^ secret_num) % 16777216
        secret_num = ((secret_num // 32) ^ secret_num) % 16777216
        secret_num = ((secret_num * 2048) ^ secret_num) % 16777216


def part_1() -> None:
    print(sum(next(islice(calculate_secret_numbers(secret_num), 2000, 2001)) for secret_num in secret_nums))


def part_2() -> None:
    all_prices = [
        tuple(num % 10 for num in islice(calculate_secret_numbers(secret_num), 2001)) for secret_num in secret_nums
    ]
    all_price_changes = [tuple(num_2 - num_1 for num_1, num_2 in pairwise(buyer_prices)) for buyer_prices in all_prices]
    all_windows_to_prices = [
        {window: prices[2000 - i] for i, window in enumerate(reversed(list(sliding_window(price_changes, 4))))}
        for price_changes, prices in zip(all_price_changes, all_prices)
    ]
    max_bananas = 0
    for window_target in product(range(-9, 10), repeat=4):
        total_differences = tuple(accumulate(window_target))
        if any(w > 9 for w in total_differences) or any(w < -9 for w in total_differences):
            continue
        bananas = 0
        for windows_to_prices in all_windows_to_prices:  # ~3s faster than comprehension, not sure why
            bananas += windows_to_prices.get(window_target, 0)
        if bananas > max_bananas:
            max_bananas = bananas
    print(max_bananas)
