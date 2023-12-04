with open('./2023/resources/4.txt') as f:
    lines = [line.strip() for line in f]


def problem_1() -> None:
    total_points = 0
    for line in lines:
        all_nums = line.split(": ")[1]
        all_winning_nums, all_have_nums = all_nums.split(" | ")
        winning_nums = {int(n) for n in all_winning_nums.split()}
        have_nums = {int(n) for n in all_have_nums.split()}
        num_found = len(winning_nums & have_nums)
        total_points += 2 ** (num_found - 1) if num_found != 0 else 0
    print(total_points)


def problem_2() -> None:
    total_cards = {i: 1 for i in range(1, len(lines) + 1)}
    for line in lines:
        card_info, all_nums = line.split(": ")
        card_number = int(card_info.split()[1])
        all_winning_nums, all_have_nums = all_nums.split(" | ")
        winning_nums = {int(n) for n in all_winning_nums.split()}
        have_nums = {int(n) for n in all_have_nums.split()}
        num_found = len(winning_nums & have_nums)
        for i in range(1, num_found + 1):
            total_cards[card_number + i] += total_cards[card_number]
    print(sum(total_cards.values()))
