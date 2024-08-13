with open("./2019/resources/16.txt") as f:
    input_num = [int(char) for char in f.read().strip()]


def fft(input_num: list[int]) -> list[int]:
    n = len(input_num)
    positive_sum_indices: dict[int, list[tuple[int, int]]] = {}
    negative_sum_indices: dict[int, list[tuple[int, int]]] = {}
    for i in range(n):
        positive_groups = [(j, j + i) for j in range(i, n, 4 * (i + 1))]
        negative_groups = [(j, j + i) for j in range(3 * i + 2, n, 4 * (i + 1))]
        positive_groups[-1] = (min(positive_groups[-1][0], n - 1), min(positive_groups[-1][1], n - 1))
        if negative_groups:
            negative_groups[-1] = (min(negative_groups[-1][0], n - 1), min(negative_groups[-1][1], n - 1))
        positive_sum_indices[i] = positive_groups
        negative_sum_indices[i] = negative_groups

    numbers = input_num
    for _ in range(100):
        partial_sums = [0 for _ in range(n + 1)]
        for i in range(n):
            partial_sums[i + 1] = partial_sums[i] + numbers[i]
        new_numbers = [0 for _ in range(n)]
        for i in range(n):
            positive_total = sum(
                partial_sums[group_end + 1] - partial_sums[group_start]
                for (group_start, group_end) in positive_sum_indices[i]
            )
            negative_total = sum(
                partial_sums[group_end + 1] - partial_sums[group_start]
                for (group_start, group_end) in negative_sum_indices[i]
            )
            new_numbers[i] = abs(positive_total - negative_total) % 10
        numbers = new_numbers
    return numbers


def fft_second_half_only(input_num: list[int]) -> list[int]:
    n = len(input_num) // 2
    numbers = input_num[n:]
    for _ in range(100):
        new_numbers = [0 for _ in range(n)]
        new_numbers[-1] = numbers[-1]
        for i in range(1, n):
            new_numbers[n - i - 1] = (new_numbers[n - i] + numbers[n - i - 1]) % 10
        numbers = new_numbers
    return numbers


def problem_1() -> None:
    output = fft(input_num)
    print("".join(str(x) for x in output[:8]))


def problem_2() -> None:
    message_offset = int("".join(str(x) for x in input_num[:7])) - ((len(input_num) * 10000) // 2)
    assert message_offset >= 0
    output = fft_second_half_only(input_num * 10000)
    print("".join(str(x) for x in output[message_offset : message_offset + 8]))
