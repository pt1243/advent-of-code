from collections.abc import Iterator, Sequence
from typing import NamedTuple


with open('./2015/resources/15.txt') as f:
    ingredients_data = [line.strip() for line in f]


class Ingredient(NamedTuple):
    name: str
    capacity: int
    durability: int
    flavour: int
    texture: int
    calories: int


def sum_to(total: int, num_items: int) -> Iterator[list[int]]:
    if num_items == 1:
        yield [total]
    else:
        for i in range(total+1):
            for rest in sum_to(total - i, num_items - 1):
                yield [i] + rest


def problem_1():
    possible_ingredients: list[Ingredient] = []
    for ingredient in ingredients_data:
        name = ingredient.split(":")[0]
        capacity = int(ingredient[ingredient.index("capacity")+9:ingredient.index("durability")-2])
        durability = int(ingredient[ingredient.index("durability")+11:ingredient.index("flavor")-2])
        flavour = int(ingredient[ingredient.index("flavor")+7:ingredient.index("texture")-2])
        texture = int(ingredient[ingredient.index("texture")+8:ingredient.index("calories")-2])
        calories = int(ingredient[ingredient.index("calories")+9:])
        possible_ingredients.append(Ingredient(name, capacity, durability, flavour, texture, calories))

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


def problem_2():
    possible_ingredients: list[Ingredient] = []
    for ingredient in ingredients_data:
        name = ingredient.split(":")[0]
        capacity = int(ingredient[ingredient.index("capacity")+9:ingredient.index("durability")-2])
        durability = int(ingredient[ingredient.index("durability")+11:ingredient.index("flavor")-2])
        flavour = int(ingredient[ingredient.index("flavor")+7:ingredient.index("texture")-2])
        texture = int(ingredient[ingredient.index("texture")+8:ingredient.index("calories")-2])
        calories = int(ingredient[ingredient.index("calories")+9:])
        possible_ingredients.append(Ingredient(name, capacity, durability, flavour, texture, calories))

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
