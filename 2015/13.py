from itertools import permutations


with open('./2015/resources/13.txt') as f:
    lines = [line.strip() for line in f]


def problem_1() -> None:
    happiness_by_person: dict[str, dict[str, int]] = {}

    for line in lines:
        person_from = line.split(maxsplit=1)[0]
        if person_from not in happiness_by_person:
            happiness_by_person[person_from] = {}
        person_to = line.rsplit(maxsplit=1)[1].removesuffix(".")
        if "lose" in line:
            happiness = -int(line[line.index("lose") + 5 : line.index("happiness")])
        else:
            happiness = int(line[line.index("gain") + 5 : line.index("happiness")])
        happiness_by_person[person_from][person_to] = happiness

    max_happiness: int | None = None
    for perm in permutations(happiness_by_person):
        happiness = 0
        for idx, person in enumerate(perm):
            if idx == 0:
                happiness += happiness_by_person[person][perm[1]]
                happiness += happiness_by_person[person][perm[-1]]
            elif idx == 7:
                happiness += happiness_by_person[person][perm[6]]
                happiness += happiness_by_person[person][perm[0]]
            else:
                happiness += happiness_by_person[person][perm[idx - 1]]
                happiness += happiness_by_person[person][perm[idx + 1]]
        if max_happiness is None or happiness > max_happiness:
            max_happiness = happiness
    print(max_happiness)


def problem_2() -> None:
    happiness_by_person: dict[str, dict[str, int]] = {}

    for line in lines:
        person_from = line.split(maxsplit=1)[0]
        if person_from not in happiness_by_person:
            happiness_by_person[person_from] = {}
        person_to = line.rsplit(maxsplit=1)[1].removesuffix(".")
        if "lose" in line:
            happiness = -int(line[line.index("lose") + 5 : line.index("happiness")])
        else:
            happiness = int(line[line.index("gain") + 5 : line.index("happiness")])
        happiness_by_person[person_from][person_to] = happiness

    people = list(happiness_by_person.keys())
    for relationships in happiness_by_person.values():
        relationships["me"] = 0
    happiness_by_person["me"] = {p: 0 for p in people}

    max_happiness: int | None = None
    for perm in permutations(happiness_by_person):
        happiness = 0
        for idx, person in enumerate(perm):
            if idx == 0:
                happiness += happiness_by_person[person][perm[1]]
                happiness += happiness_by_person[person][perm[-1]]
            elif idx == 8:
                happiness += happiness_by_person[person][perm[7]]
                happiness += happiness_by_person[person][perm[0]]
            else:
                happiness += happiness_by_person[person][perm[idx - 1]]
                happiness += happiness_by_person[person][perm[idx + 1]]
        if max_happiness is None or happiness > max_happiness:
            max_happiness = happiness
    print(max_happiness)
