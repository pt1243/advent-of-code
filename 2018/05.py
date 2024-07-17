from string import ascii_lowercase, ascii_uppercase


with open("./2018/resources/5.txt") as f:
    starting_polymer = f.read().strip()


def problem_1() -> None:
    polymer = starting_polymer
    start_index = 0
    while True:
        changed = False
        for i, (c1, c2) in enumerate(zip(polymer[start_index:-1], polymer[1 + start_index :]), start=start_index):
            if c1.lower() == c2.lower() and ((c1.isupper() and c2.islower()) or (c1.islower() and c2.isupper())):
                polymer = polymer[:i] + polymer[i + 2 :]
                start_index = max(i - 1, 0)
                changed = True
                break
        if not changed:
            break
    print(len(polymer))


def problem_2() -> None:
    min_length = len(starting_polymer)
    for lower, upper in zip(ascii_lowercase, ascii_uppercase):
        polymer = starting_polymer.replace(lower, "").replace(upper, "")
        start_index = 0
        while True:
            changed = False
            for i, (c1, c2) in enumerate(zip(polymer[start_index:-1], polymer[1 + start_index :]), start=start_index):
                if c1.lower() == c2.lower() and ((c1.isupper() and c2.islower()) or (c1.islower() and c2.isupper())):
                    polymer = polymer[:i] + polymer[i + 2 :]
                    start_index = max(i - 1, 0)
                    changed = True
                    break
            if not changed:
                break
        min_length = min(len(polymer), min_length)
    print(min_length)
