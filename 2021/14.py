from collections import defaultdict
from itertools import pairwise

with open("./2021/resources/14.txt") as f:
    text = f.read().strip()


def run_pair_insertion_process(steps: int) -> int:
    polymer_template, all_rules = text.split("\n\n")
    start_char = polymer_template[0]
    end_char = polymer_template[-1]

    rules: dict[str, tuple[str, str]] = {}
    for rule in all_rules.split("\n"):
        left, right = rule.split(" -> ")
        rules[left] = (left[0] + right, right + left[1])

    current_counts: defaultdict[str, int] = defaultdict(int)
    for pair_string in pairwise(polymer_template):
        current_counts[pair_string[0] + pair_string[1]] += 1

    for _ in range(steps):
        new_counts: defaultdict[str, int] = defaultdict(int)
        for pair, count in current_counts.items():
            replacements = rules[pair]
            new_counts[replacements[0]] += count
            new_counts[replacements[1]] += count
        current_counts = new_counts

    letter_counts: defaultdict[str, int] = defaultdict(int)
    for pair, count in current_counts.items():
        letter_counts[pair[0]] += count
        letter_counts[pair[1]] += count
    letter_counts[start_char] += 1
    letter_counts[end_char] += 1
    return (max(letter_counts.values()) - min(letter_counts.values())) // 2


def problem_1() -> None:
    print(run_pair_insertion_process(10))


def problem_2() -> None:
    print(run_pair_insertion_process(40))
