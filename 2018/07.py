from collections import defaultdict
from itertools import count

with open("./2018/resources/7.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    all_letters_set: set[str] = set()
    prerequisites: defaultdict[str, list[str]] = defaultdict(list)
    for line in lines:
        first, second = line.split()[1], line.split()[7]
        all_letters_set.add(first)
        all_letters_set.add(second)
        prerequisites[second].append(first)
    all_letters = sorted(all_letters_set)
    completed = {letter: False for letter in all_letters}
    result = ""
    while True:
        for letter in all_letters:
            if completed[letter]:
                continue
            if all(completed[prereq] for prereq in prerequisites[letter]):
                completed[letter] = True
                result += letter
                break
        if all(completed.values()):
            break
    print(result)


def problem_2() -> None:
    all_letters_set: set[str] = set()
    prerequisites: defaultdict[str, list[str]] = defaultdict(list)
    for line in lines:
        first, second = line.split()[1], line.split()[7]
        all_letters_set.add(first)
        all_letters_set.add(second)
        prerequisites[second].append(first)
    all_letters = sorted(all_letters_set)
    completed = {letter: False for letter in all_letters}
    total_workers = 5
    currently_working_on: dict[int, str | None] = {i: None for i in range(total_workers)}
    time_remaining = {letter: ord(letter) - ord("A") + 61 for letter in all_letters}

    for step in count():
        for worker in range(total_workers):
            current_letter = currently_working_on[worker]
            if current_letter:
                time_remaining[current_letter] -= 1
                if time_remaining[current_letter] == 0:
                    currently_working_on[worker] = None
                    completed[current_letter] = True

        available_letters = [
            letter
            for letter in all_letters
            if not completed[letter]
            and all(completed[prereq] for prereq in prerequisites[letter])
            and letter not in currently_working_on.values()
        ]
        if (
            all(current_letter is None for current_letter in currently_working_on.values())
            and not available_letters
            and all(completed.keys())
        ):
            print(step)
            return

        for worker, available_letter in zip(
            [i for i in range(total_workers) if not currently_working_on[i]], available_letters
        ):
            currently_working_on[worker] = available_letter
