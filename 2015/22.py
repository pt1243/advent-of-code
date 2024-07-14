import heapq
from typing import NamedTuple


with open("./2015/resources/22.txt") as f:
    lines = [line.strip() for line in f]

starting_player_hp = 50
starting_player_mana = 500
starting_boss_hp = int(lines[0].split(": ")[1])
boss_damage = int(lines[1].split(": ")[1])


class State(NamedTuple):
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


def evaluate_cost(spells: tuple[str, ...], part_2: bool = False) -> tuple[int, State | None, bool]:
    player_hp = starting_player_hp
    player_mana = starting_player_mana
    boss_hp = starting_boss_hp
    shield_timer = 0
    poison_timer = 0
    recharge_timer = 0

    spent_mana = 0

    def apply_effects():
        nonlocal player_mana, boss_hp, shield_timer, poison_timer, recharge_timer
        if shield_timer > 0:
            shield_timer -= 1
        if poison_timer > 0:
            boss_hp -= 3
            poison_timer -= 1
        if recharge_timer > 0:
            player_mana += 101
            recharge_timer -= 1

    for spell in spells:
        # before player turn
        if part_2:
            player_hp -= 1
            if player_hp <= 0:
                return 0, None, False
        apply_effects()
        if boss_hp <= 0:
            return spent_mana, None, True

        # player turn
        if spell == "magic missile":
            spent_mana += 53
            player_mana -= 53
            boss_hp -= 4
        elif spell == "drain":
            spent_mana += 73
            player_mana -= 73
            boss_hp -= 2
            player_hp += 2
        elif spell == "shield":
            if shield_timer > 0:
                return 0, None, False
            spent_mana += 113
            player_mana -= 113
            shield_timer = 6
        elif spell == "poison":
            if poison_timer > 0:
                return 0, None, False
            spent_mana += 173
            player_mana -= 173
            poison_timer = 6
        elif spell == "recharge":
            if recharge_timer > 0:
                return 0, None, False
            spent_mana += 229
            player_mana -= 229
            recharge_timer = 5

        # if player did not have enough to cast the last spell
        if player_mana < 0:
            return 0, None, False

        # boss turn
        apply_effects()
        if boss_hp <= 0:
            return spent_mana, None, True

        armor = 7 if shield_timer > 0 else 0
        player_hp -= max(boss_damage - armor, 1)
        if player_hp <= 0:
            return 0, None, False

    # continue playing
    return spent_mana, State(player_hp, player_mana, boss_hp, shield_timer, poison_timer, recharge_timer), False


def problem_1() -> None:
    possibilities = []
    for spell, cost in spell_costs.items():
        heapq.heappush(possibilities, (cost, (spell,), False))
    while True:
        cost, spells, victory = heapq.heappop(possibilities)
        if victory:
            print(cost)
            return
        for new_spell in spell_costs.keys():
            new_spells = (*spells, new_spell)
            new_cost, state, victory = evaluate_cost(new_spells)
            if victory or (state is not None):
                heapq.heappush(possibilities, (new_cost, new_spells, victory))


def problem_2() -> None:
    possibilities = []
    for spell, cost in spell_costs.items():
        heapq.heappush(possibilities, (cost, (spell,), False))
    while True:
        cost, spells, victory = heapq.heappop(possibilities)
        if victory:
            print(cost)
            return
        for new_spell in spell_costs.keys():
            new_spells = (*spells, new_spell)
            new_cost, state, victory = evaluate_cost(new_spells, part_2=True)
            if victory or (state is not None):
                heapq.heappush(possibilities, (new_cost, new_spells, victory))
