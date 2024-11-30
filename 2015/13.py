from itertools import permutations
from collections import defaultdict
from typing import MutableMapping


with open("./2015/resources/13.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    happiness_by_person: defaultdict[str, defaultdict[str, int]] = defaultdict(lambda: defaultdict(int))
    for line in lines:
        split = line.split()
        person_from = split[0]
        person_to = split[10].strip(".")
        happiness = (1 if "gain" in line else -1) * int(split[3])
        happiness_by_person[person_from][person_to] = happiness

    max_happiness = 0
    num_people = len(happiness_by_person)
    for perm in permutations(happiness_by_person):
        happiness = 0
        for idx, person in enumerate(perm):
            happiness += happiness_by_person[person][perm[(idx - 1) % num_people]]
            happiness += happiness_by_person[person][perm[(idx + 1) % num_people]]
        max_happiness = max(max_happiness, happiness)

    print(max_happiness)


def problem_2() -> None:
    happiness_by_person: defaultdict[str, MutableMapping[str, int]] = defaultdict(lambda: defaultdict(int))
    for line in lines:
        split = line.split()
        person_from = split[0]
        person_to = split[10].strip(".")
        happiness = (1 if "gain" in line else -1) * int(split[3])
        happiness_by_person[person_from][person_to] = happiness

    people = list(happiness_by_person.keys())
    for relationships in happiness_by_person.values():
        relationships["me"] = 0
    happiness_by_person["me"] = {p: 0 for p in people}

    max_happiness = 0
    num_people = len(happiness_by_person)
    for perm in permutations(happiness_by_person):
        happiness = 0
        for idx, person in enumerate(perm):
            happiness += happiness_by_person[person][perm[(idx - 1) % num_people]]
            happiness += happiness_by_person[person][perm[(idx + 1) % num_people]]
        max_happiness = max(max_happiness, happiness)

    print(max_happiness)
