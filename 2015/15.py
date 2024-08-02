from collections.abc import Iterator
from typing import NamedTuple


with open("./2015/resources/15.txt") as f:
    ingredients_data = f.read().splitlines()


class Ingredient(NamedTuple):
    name: str
    capacity: int
    durability: int
    flavour: int
    texture: int
    calories: int


def process_ingredients() -> list[Ingredient]:
    possible_ingredients: list[Ingredient] = []
    for ingredient_text in ingredients_data:
        name = ingredient_text.split(":")[0]
        capacity = int(ingredient_text[ingredient_text.index("capacity") + 9 : ingredient_text.index("durability") - 2])
        durability = int(
            ingredient_text[ingredient_text.index("durability") + 11 : ingredient_text.index("flavor") - 2]
        )
        flavour = int(ingredient_text[ingredient_text.index("flavor") + 7 : ingredient_text.index("texture") - 2])
        texture = int(ingredient_text[ingredient_text.index("texture") + 8 : ingredient_text.index("calories") - 2])
        calories = int(ingredient_text[ingredient_text.index("calories") + 9 :])
        possible_ingredients.append(Ingredient(name, capacity, durability, flavour, texture, calories))
    return possible_ingredients


def sum_to(total: int, num_items: int) -> Iterator[list[int]]:
    if num_items == 1:
        yield [total]
    else:
        for i in range(total + 1):
            for rest in sum_to(total - i, num_items - 1):
                yield [i] + rest


def problem_1() -> None:
    possible_ingredients = process_ingredients()

    max_found = None
    for combination in sum_to(100, len(possible_ingredients)):
        capacity = 0
        durability = 0
        flavour = 0
        texture = 0
        for idx, number in enumerate(combination):
            ingredient = possible_ingredients[idx]
            capacity += number * ingredient.capacity
            durability += number * ingredient.durability
            flavour += number * ingredient.flavour
            texture += number * ingredient.texture
        capacity = max(capacity, 0)
        durability = max(durability, 0)
        flavour = max(flavour, 0)
        texture = max(texture, 0)
        total = capacity * durability * flavour * texture
        if max_found is None or total > max_found:
            max_found = total

    print(max_found)


def problem_2() -> None:
    possible_ingredients = process_ingredients()

    max_found = None
    for combination in sum_to(100, len(possible_ingredients)):
        capacity = 0
        durability = 0
        flavour = 0
        texture = 0
        calories = 0
        for idx, number in enumerate(combination):
            ingredient = possible_ingredients[idx]
            capacity += number * ingredient.capacity
            durability += number * ingredient.durability
            flavour += number * ingredient.flavour
            texture += number * ingredient.texture
            calories += number * ingredient.calories
        if calories != 500:
            continue
        capacity = max(capacity, 0)
        durability = max(durability, 0)
        flavour = max(flavour, 0)
        texture = max(texture, 0)
        total = capacity * durability * flavour * texture
        if max_found is None or total > max_found:
            max_found = total

    print(max_found)
