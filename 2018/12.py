with open("./2018/resources/12.txt") as f:
    text = f.read().strip()


def part_1() -> None:
    initial_state, all_rules = text.split("\n\n")
    state = [True if char == "#" else False for char in initial_state.split(": ")[1]]
    rules: dict[tuple[bool, ...], bool] = {}
    for rule in all_rules.split("\n"):
        lhs, rhs = rule.split(" => ")
        rules[tuple([True if char == "#" else False for char in lhs])] = True if rhs == "#" else False

    min_index = 0
    for _ in range(20):
        new_state: list[bool] = []
        for i in range(-2, len(state) + 2):
            if i < 2:
                seeds_to_check = [False] * (2 - i) + state[: i + 3]
                if rules[tuple(seeds_to_check)]:
                    new_state.append(True)
                    if i < 0:
                        min_index -= 1
                elif i >= 0:
                    new_state.append(False)
            elif i >= len(state) - 2:
                seeds_to_check = state[i - 2 :] + [False] * (3 + i - len(state))
                if rules[tuple(seeds_to_check)]:
                    new_state.append(True)
                elif i < len(state):
                    new_state.append(False)
            else:
                new_state.append(rules[tuple(state[i - 2 : i + 3])])
        state = new_state
    print(sum(i for i, plant in enumerate(state, start=min_index) if plant))


def part_2() -> None:
    initial_state, all_rules = text.split("\n\n")
    state = [True if char == "#" else False for char in initial_state.split(": ")[1]]
    rules: dict[tuple[bool, ...], bool] = {}
    for rule in all_rules.split("\n"):
        lhs, rhs = rule.split(" => ")
        rules[tuple([True if char == "#" else False for char in lhs])] = True if rhs == "#" else False

    min_index = 0
    last = 0
    totals = [sum(i for i, plant in enumerate(state, start=min_index) if plant)]
    differences = [0]
    for _ in range(200):
        new_state: list[bool] = []
        for i in range(-2, len(state) + 2):
            if i < 2:
                seeds_to_check = [False] * (2 - i) + state[: i + 3]
                if rules[tuple(seeds_to_check)]:
                    new_state.append(True)
                    if i < 0:
                        min_index -= 1
                elif i >= 0:
                    new_state.append(False)
            elif i >= len(state) - 2:
                seeds_to_check = state[i - 2 :] + [False] * (3 + i - len(state))
                if rules[tuple(seeds_to_check)]:
                    new_state.append(True)
                elif i < len(state):
                    new_state.append(False)
            else:
                new_state.append(rules[tuple(state[i - 2 : i + 3])])
        state = new_state
        total = sum(i for i, plant in enumerate(state, start=min_index) if plant)
        totals.append(total)
        differences.append(total - last)
        last = total

    consistent_difference = differences[-1]
    last_inconsistent_index = max([i for i, d in enumerate(differences) if d != consistent_difference])
    print((50_000_000_000 - last_inconsistent_index) * consistent_difference + totals[last_inconsistent_index])
