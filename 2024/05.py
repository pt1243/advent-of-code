from collections import defaultdict
from itertools import combinations


with open("./2024/resources/5.txt") as f:
    text = f.read().strip()


def problem_1() -> None:
    rules_text, manuals = text.split("\n\n")
    rules: set[tuple[int, int]] = set()
    for line in rules_text.split("\n"):
        first, second = line.split("|")
        rules.add((int(first), int(second)))

    total = 0
    for line in manuals.split("\n"):
        in_right_order = True
        pages = [int(x) for x in line.split(",")]
        for page_1, page_2 in combinations(pages, 2):
            if (page_2, page_1) in rules:
                in_right_order = False
                break
        if in_right_order:
            total += pages[len(pages) // 2]
    print(total)


def problem_2() -> None:
    rules_text, manuals = text.split("\n\n")
    rules: set[tuple[int, int]] = set()
    for line in rules_text.split("\n"):
        first, second = line.split("|")
        rules.add((int(first), int(second)))

    nums_before: defaultdict[int, set[int]] = defaultdict(set)
    for left, right in rules:
        nums_before[right].add(left)

    total = 0
    for line in manuals.split("\n"):
        in_right_order = True
        nums = [int(x) for x in line.split(",")]
        for page_1, page_2 in combinations(nums, 2):
            if (page_2, page_1) in rules:
                in_right_order = False
                break

        if not in_right_order:
            for i in range(len(nums)):  # insertion sort
                for j in range(i, 0, -1):
                    if nums[j - 1] not in nums_before[nums[j]]:
                        break
                    nums[j], nums[j - 1] = nums[j - 1], nums[j]

            total += nums[len(nums) // 2]
    print(total)
