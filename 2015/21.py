from itertools import product, combinations
from typing import NamedTuple


with open("./2015/resources/21.txt") as f:
    lines = f.read().splitlines()
    starting_boss_hp = int(lines[0].split(": ")[1])
    boss_damage = int(lines[1].split(": ")[1])
    boss_armour = int(lines[2].split(": ")[1])


class Item(NamedTuple):
    name: str
    cost: int
    damage: int
    armour: int


weapon_choices = (
    Item("Dagger", 8, 4, 0),
    Item("Shortsword", 10, 5, 0),
    Item("Warhammer", 25, 6, 0),
    Item("Longsword", 40, 7, 0),
    Item("Greataxe", 74, 8, 0),
)


armour_choices = (
    Item("No armour", 0, 0, 0),
    Item("Leather", 13, 0, 1),
    Item("Chainmail", 31, 0, 2),
    Item("Splintmail", 53, 0, 3),
    Item("Bandedmail", 75, 0, 4),
    Item("Platemail", 102, 0, 5),
)


rings = (
    Item("Damage +1", 25, 1, 0),
    Item("Damage +2", 50, 2, 0),
    Item("Damage +3", 100, 3, 0),
    Item("Defense +1", 20, 0, 1),
    Item("Defense +2", 40, 0, 2),
    Item("Defense +3", 80, 0, 3),
)


ring_choices = (
    Item("No rings", 0, 0, 0),
    *(r for r in rings),  # one ring
    *(
        Item(r1.name + " and " + r2.name, r1.cost + r2.cost, r1.damage + r2.damage, r1.armour + r2.armour)
        for r1, r2 in combinations(rings, 2)
    ),  # two rings
)


def simulate(player_hp: int, player_damage: int, player_armour: int) -> bool:
    player_turn = True
    boss_hp = starting_boss_hp
    while boss_hp > 0 and player_hp > 0:
        if player_turn:
            damage = max(player_damage - boss_armour, 1)
            boss_hp -= damage
            player_turn = False
        else:
            damage = max(boss_damage - player_armour, 1)
            player_hp -= damage
            player_turn = True
    return player_hp > 0


def problem_1() -> None:
    min_cost = float("inf")
    for weapon, armour, ring_combo in product(weapon_choices, armour_choices, ring_choices):
        total_cost = weapon.cost + armour.cost + ring_combo.cost
        total_damage = weapon.damage + armour.damage + ring_combo.damage
        total_armour = weapon.armour + armour.armour + ring_combo.armour

        if simulate(100, total_damage, total_armour):
            if total_cost < min_cost:
                min_cost = total_cost

    print(min_cost)


def problem_2() -> None:
    max_cost = 0
    for weapon, armour, ring_combo in product(weapon_choices, armour_choices, ring_choices):
        total_cost = weapon.cost + armour.cost + ring_combo.cost
        total_damage = weapon.damage + armour.damage + ring_combo.damage
        total_armour = weapon.armour + armour.armour + ring_combo.armour

        if not simulate(100, total_damage, total_armour):
            if total_cost > max_cost:
                max_cost = total_cost

    print(max_cost)
