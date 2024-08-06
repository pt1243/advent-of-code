with open("./2019/resources/14.txt") as f:
    lines = f.read().splitlines()


def get_ore_required(num_fuel: int) -> int:
    reactions: dict[str, tuple[int, int, list[tuple[str, int]]]] = {}
    for line in lines:
        left, right = line.split(" => ")
        left_items = left.split(", ")
        produced_qty, output = right.split()
        reactants: list[tuple[str, int]] = []
        ore_consumed = 0
        for input_item in left_items:
            reactant_qty, reactant = input_item.split()
            if reactant == "ORE":
                ore_consumed = int(reactant_qty)
            else:
                reactants.append((reactant, int(reactant_qty)))
        reactions[output] = (int(produced_qty), ore_consumed, reactants)

    current = {product: 0 for product in reactions.keys()}
    ore_used = 0
    for reactant, qty in reactions["FUEL"][2]:
        current[reactant] = -qty * num_fuel

    while any(v < 0 for v in current.values()):
        item_to_produce = [item for item, qty in current.items() if qty < 0][0]
        output_qty, ore_consumed, input_items = reactions[item_to_produce]
        full_reactions, mod = divmod(abs(current[item_to_produce]), output_qty)
        if mod:
            full_reactions += 1
        current[item_to_produce] += output_qty * full_reactions
        ore_used += ore_consumed * full_reactions
        for input_item, input_qty in input_items:
            current[input_item] -= input_qty * full_reactions
    return ore_used


def problem_1() -> None:
    print(get_ore_required(1))


def problem_2() -> None:
    max_safe_val = 0
    step = 1_000_000
    steps_up = 0
    while True:
        current_val = max_safe_val + steps_up * step
        ore_required = get_ore_required(current_val)
        steps_up += 1
        if ore_required > 1_000_000_000_000:
            if step == 1:
                print(current_val - 1)
                return
            max_safe_val = current_val - step
            step //= 10
            steps_up = 0
