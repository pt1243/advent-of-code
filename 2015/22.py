import heapq
from typing import NamedTuple


with open("./2015/resources/22.txt") as f:
    lines = f.read().splitlines()
    starting_player_hp = 50
    starting_player_mana = 500
    starting_boss_hp = int(lines[0].split(": ")[1])
    boss_damage = int(lines[1].split(": ")[1])


class State(NamedTuple):
    spent_mana: int
    player_hp: int
    player_mana: int
    boss_hp: int
    shield_timer: int
    poison_timer: int
    recharge_timer: int


spell_costs = {
    "magic missile": 53,
    "drain": 73,
    "shield": 113,
    "poison": 173,
    "recharge": 229,
}


def apply_spell(state: State, spell: str, part_2: bool = False) -> State | bool:
    spent_mana, player_hp, player_mana, boss_hp, shield_timer, poison_timer, recharge_timer = state

    # before player turn
    if part_2:
        player_hp -= 1
        if player_hp <= 0:
            return False

    # apply timer effects
    shield_timer = max(shield_timer - 1, 0)
    if poison_timer > 0:
        boss_hp -= 3
    poison_timer = max(poison_timer - 1, 0)
    if recharge_timer > 0:
        player_mana += 101
    recharge_timer = max(recharge_timer - 1, 0)

    if boss_hp <= 0:
        return True

    # player turn
    spent_mana += spell_costs[spell]
    player_mana -= spell_costs[spell]

    if player_mana < 0:
        return False

    if spell == "magic missile":
        boss_hp -= 4
    elif spell == "drain":
        boss_hp -= 2
        player_hp += 2
    elif spell == "shield":
        if shield_timer > 0:
            return False
        shield_timer = 6
    elif spell == "poison":
        if poison_timer > 0:
            return False
        poison_timer = 6
    elif spell == "recharge":
        if recharge_timer > 0:
            return False
        recharge_timer = 5

    if boss_hp <= 0:
        return True

    # boss turn
    # apply timer effects
    shield_timer = max(shield_timer - 1, 0)
    if poison_timer > 0:
        boss_hp -= 3
    poison_timer = max(poison_timer - 1, 0)
    if recharge_timer > 0:
        player_mana += 101
    recharge_timer = max(recharge_timer - 1, 0)

    if boss_hp <= 0:
        return True

    armour = 7 if shield_timer > 0 else 0
    player_hp -= max(boss_damage - armour, 1)
    if player_hp <= 0:
        return False

    return State(spent_mana, player_hp, player_mana, boss_hp, shield_timer, poison_timer, recharge_timer)


def problem_1() -> None:
    possibilities = [(State(0, starting_player_hp, starting_player_mana, starting_boss_hp, 0, 0, 0), False)]
    seen: set[State] = set()
    while True:
        state, victory = heapq.heappop(possibilities)
        if victory:
            print(state.spent_mana)
            return
        for spell, cost in spell_costs.items():
            result = apply_spell(state, spell)
            if result is False:  # lost the fight or invalid spell
                continue
            if result is True:  # victory
                heapq.heappush(possibilities, (state._replace(spent_mana=state.spent_mana + cost), True))
            else:  # no result yet
                if result in seen:
                    continue
                seen.add(result)
                heapq.heappush(possibilities, (result, False))


def problem_2() -> None:
    possibilities = [(State(0, starting_player_hp, starting_player_mana, starting_boss_hp, 0, 0, 0), False)]
    seen: set[State] = set()
    while True:
        state, victory = heapq.heappop(possibilities)
        if victory:
            print(state.spent_mana)
            return
        for spell, cost in spell_costs.items():
            result = apply_spell(state, spell, part_2=True)
            if result is False:  # lost the fight or invalid spell
                continue
            if result is True:  # victory
                heapq.heappush(possibilities, (state._replace(spent_mana=state.spent_mana + cost), True))
            else:  # no result yet
                if result in seen:
                    continue
                seen.add(result)
                heapq.heappush(possibilities, (result, False))
