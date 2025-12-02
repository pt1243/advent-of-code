from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from itertools import count
from operator import attrgetter
from typing import Literal

with open("./2018/resources/24.txt") as f:
    input_text = f.read().strip()


@dataclass
class Group:
    army: Literal["immune system", "infection"]
    units: int
    hp: int
    immunities: set[str]
    weaknesses: set[str]
    attack_damage: int
    attack_type: str
    initiative: int
    targeted: bool = False
    target: Group | None = None

    @property
    def effective_power(self) -> int:
        return self.units * self.attack_damage


def parse_input(text: str) -> list[Group]:
    groups = []
    immune_system_groups_text, infection_groups_text = text.split("\n\n")
    for line in immune_system_groups_text.split("\n")[1:]:
        split = line.split()
        units = int(split[0])
        hp = int(split[4])
        if "(" in line:
            weaknesses_and_immunities = line[line.index("(") + 1 : line.index(")")].split("; ")
            if len(weaknesses_and_immunities) == 1:
                items = set(item.rstrip(",") for item in weaknesses_and_immunities[0].split()[2:])
                if weaknesses_and_immunities[0].startswith("weak"):
                    weaknesses, immunities = items, set()
                else:
                    weaknesses, immunities = set(), items
            else:
                first_items = set(item.rstrip(",") for item in weaknesses_and_immunities[0].split()[2:])
                second_items = set(item.rstrip(",") for item in weaknesses_and_immunities[1].split()[2:])
                if weaknesses_and_immunities[0].startswith("weak"):
                    weaknesses, immunities = first_items, second_items
                else:
                    weaknesses, immunities = second_items, first_items
        else:
            weaknesses, immunities = set(), set()
        attack_damage = int(split[-6])
        attack_type = split[-5]
        initiative = int(split[-1])
        groups.append(Group("immune system", units, hp, immunities, weaknesses, attack_damage, attack_type, initiative))
    for line in infection_groups_text.split("\n")[1:]:
        split = line.split()
        units = int(split[0])
        hp = int(split[4])
        if "(" in line:
            weaknesses_and_immunities = line[line.index("(") + 1 : line.index(")")].split("; ")
            if len(weaknesses_and_immunities) == 1:
                items = set(item.rstrip(",") for item in weaknesses_and_immunities[0].split()[2:])
                if weaknesses_and_immunities[0].startswith("weak"):
                    weaknesses, immunities = items, set()
                else:
                    weaknesses, immunities = set(), items
            else:
                first_items = set(item.rstrip(",") for item in weaknesses_and_immunities[0].split()[2:])
                second_items = set(item.rstrip(",") for item in weaknesses_and_immunities[1].split()[2:])
                if weaknesses_and_immunities[0].startswith("weak"):
                    weaknesses, immunities = first_items, second_items
                else:
                    weaknesses, immunities = second_items, first_items
        else:
            weaknesses, immunities = set(), set()
        attack_damage = int(split[-6])
        attack_type = split[-5]
        initiative = int(split[-1])
        groups.append(Group("infection", units, hp, immunities, weaknesses, attack_damage, attack_type, initiative))
    return groups


def simulate_game(groups: list[Group], boost: int = 0) -> tuple[Literal["immune system", "infection"], int]:
    def calculate_damage(attacker: Group, defender: Group) -> int:
        if attacker.attack_type in defender.immunities:
            return 0
        elif attacker.attack_type in defender.weaknesses:
            return 2 * attacker.effective_power
        return attacker.effective_power

    for group in groups:
        if group.army == "immune system":
            group.attack_damage += boost

    while True:
        immune_system_groups = [g for g in groups if g.army == "immune system"]
        infection_groups = [g for g in groups if g.army == "infection"]
        if not immune_system_groups:
            return "infection", sum(g.units for g in infection_groups)
        if not infection_groups:
            return "immune system", sum(g.units for g in immune_system_groups)

        for group in groups:
            group.targeted = False
            group.target = None
        # order to choose targets in; effective power, then initiative
        for attacking_group in sorted(groups, key=attrgetter("army", "effective_power", "initiative"), reverse=True):
            available_targets = [g for g in groups if g.army != attacking_group.army and not g.targeted]
            if available_targets:
                best_target = available_targets[0]
                best_damage = calculate_damage(attacking_group, best_target)
                best_effective_power = best_target.effective_power
                best_initiative = best_target.initiative
                for target in available_targets[1:]:
                    use_target = False
                    damage = calculate_damage(attacking_group, target)
                    if damage > best_damage:
                        use_target = True
                    elif damage == best_damage:
                        if target.effective_power > best_effective_power:
                            use_target = True
                        elif target.effective_power == best_effective_power and target.initiative > best_initiative:
                            use_target = True
                    if use_target:
                        best_target, best_damage, best_effective_power, best_initiative = (
                            target,
                            damage,
                            target.effective_power,
                            target.initiative,
                        )
                if best_damage > 0:
                    attacking_group.target = best_target
                    best_target.targeted = True
        # attack
        if all(g.target is None for g in groups):
            # treat this as an infection victory
            return "infection", 0
        for attacking_group in sorted(groups, key=attrgetter("initiative"), reverse=True):
            if attacking_group.units <= 0 or attacking_group.target is None:
                continue
            target = attacking_group.target
            damage = calculate_damage(attacking_group, target)
            target.units -= damage // target.hp
        groups = [g for g in groups if g.units > 0]


def part_1() -> None:
    groups = parse_input(input_text)
    _, units_left = simulate_game(groups)
    print(units_left)


def part_2() -> None:
    groups = parse_input(input_text)
    for boost in count(1):
        winner, units_left = simulate_game(deepcopy(groups), boost)
        if winner == "immune system":
            print(units_left)
            return
