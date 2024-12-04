from collections import Counter, defaultdict
from copy import deepcopy


with open("./2020/resources/21.txt") as f:
    lines = f.read().splitlines()


def get_allergens(lines: list[str]) -> dict[str, str]:
    all_ingredients_per_allergen: defaultdict[str, list[set[str]]] = defaultdict(list)
    for line in lines:
        line_ingredients, line_allergens = line.strip(")").split("(contains ")
        for allergen in line_allergens.split(", "):
            all_ingredients_per_allergen[allergen].append(set(line_ingredients.split()))

    intersections: dict[str, set[str]] = {
        allergen: set.intersection(*all_ingredients)
        for allergen, all_ingredients in all_ingredients_per_allergen.items()
    }
    while any(len(possible_ingredients) > 1 for possible_ingredients in intersections.values()):
        new_intersections = deepcopy(intersections)
        for allergen, possible_ingredients in intersections.items():
            if len(possible_ingredients) == 1:
                ingredient_to_remove = possible_ingredients.pop()
                for other_allergen, other_ingredients in new_intersections.items():
                    if allergen == other_allergen:
                        continue
                    other_ingredients.discard(ingredient_to_remove)
        intersections = new_intersections

    return {allergen: possible_ingredients.pop() for allergen, possible_ingredients in intersections.items()}


def problem_1() -> None:
    allergens_to_ingredients = get_allergens(lines)

    ingredient_counts = Counter()
    for line in lines:
        line_ingredients = line.split("(contains ")[0].split()
        ingredient_counts.update(line_ingredients)

    print(
        sum(
            count
            for ingredient, count in ingredient_counts.items()
            if ingredient not in allergens_to_ingredients.values()
        )
    )


def problem_2() -> None:
    allergens_to_ingredients = get_allergens(lines)
    print(",".join(allergens_to_ingredients[val] for val in sorted(allergens_to_ingredients)))
