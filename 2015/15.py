from collections.abc import Iterator
from typing import NamedTuple

with open("./2015/resources/15.txt") as f:
    lines = f.read().splitlines()


class Ingredient(NamedTuple):
    name: str
    capacity: int
    durability: int
    flavour: int
    texture: int
    calories: int


def process_ingredients() -> list[Ingredient]:
    ingredients: list[Ingredient] = []
    for line in lines:
        split = line.split()
        name = split[0].strip(":")
        capacity = int(split[2].strip(","))
        durability = int(split[4].strip(","))
        flavour = int(split[6].strip(","))
        texture = int(split[8].strip(","))
        calories = int(split[10].strip(","))
        ingredients.append(Ingredient(name, capacity, durability, flavour, texture, calories))
    return ingredients


def sum_to(total: int, num_items: int) -> Iterator[list[int]]:
    if num_items == 1:
        yield [total]
    else:
        for i in range(total + 1):
            for rest in sum_to(total - i, num_items - 1):
                yield [i] + rest


def part_1() -> None:
    possible_ingredients = process_ingredients()

    max_score = 0
    for combination in sum_to(100, len(possible_ingredients)):
        capacity = 0
        durability = 0
        flavour = 0
        texture = 0
        for ingredient, number in zip(possible_ingredients, combination):
            capacity += number * ingredient.capacity
            durability += number * ingredient.durability
            flavour += number * ingredient.flavour
            texture += number * ingredient.texture
        capacity = max(capacity, 0)
        durability = max(durability, 0)
        flavour = max(flavour, 0)
        texture = max(texture, 0)
        total = capacity * durability * flavour * texture
        max_score = max(max_score, total)

    print(max_score)


def part_2() -> None:
    possible_ingredients = process_ingredients()

    max_score = 0
    for combination in sum_to(100, len(possible_ingredients)):
        capacity = 0
        durability = 0
        flavour = 0
        texture = 0
        calories = 0
        for ingredient, number in zip(possible_ingredients, combination):
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
        max_score = max(max_score, total)

    print(max_score)
