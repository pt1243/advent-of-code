import re
from itertools import islice
from math import ceil, prod
from typing import NamedTuple

with open("./2022/resources/19.txt") as f:
    lines = f.read().splitlines()


class Blueprint(NamedTuple):
    ore_robot_cost_ore: int
    clay_robot_cost_ore: int
    obsidian_robot_cost_ore: int
    obsidian_robot_cost_clay: int
    geode_robot_cost_ore: int
    geode_robot_cost_obsidian: int


class State(NamedTuple):
    ore: int
    clay: int
    obsidian: int
    geodes: int
    ore_robots: int
    clay_robots: int
    obsidian_robots: int
    geode_robots: int


def most_geodes_for_blueprint(blueprint: Blueprint, max_time: int) -> int:
    most_geodes = 0
    open_set = [(0, State(0, 0, 0, 0, 1, 0, 0, 0))]
    while open_set:
        time, state = open_set.pop()
        if time == max_time:
            if state.geodes > most_geodes:
                most_geodes = state.geodes
            continue

        # if we were able to build a geode robot every single minute until the end
        time_to_end = max_time - time
        max_possible_geodes = state.geodes + time_to_end * state.geode_robots + ((time_to_end - 1) * time_to_end // 2)
        if max_possible_geodes < most_geodes:
            continue

        # wait until end, doing nothing
        open_set.append(
            (
                max_time,
                State(
                    state.ore + state.ore_robots * time_to_end,
                    state.clay + state.clay_robots * time_to_end,
                    state.obsidian + state.obsidian_robots * time_to_end,
                    state.geodes + state.geode_robots * time_to_end,
                    state.ore_robots,
                    state.clay_robots,
                    state.obsidian_robots,
                    state.geode_robots,
                ),
            ),
        )

        # wait to buy a new ore-collecting robot
        time_to_ore_robot = max(ceil((blueprint.ore_robot_cost_ore - state.ore) / state.ore_robots) + 1, 1)
        if time + time_to_ore_robot <= max_time and state.ore_robots < max(
            blueprint.clay_robot_cost_ore, blueprint.obsidian_robot_cost_ore, blueprint.geode_robot_cost_ore
        ):
            open_set.append(
                (
                    time + time_to_ore_robot,
                    State(
                        state.ore + state.ore_robots * time_to_ore_robot - blueprint.ore_robot_cost_ore,
                        state.clay + state.clay_robots * time_to_ore_robot,
                        state.obsidian + state.obsidian_robots * time_to_ore_robot,
                        state.geodes + state.geode_robots * time_to_ore_robot,
                        state.ore_robots + 1,
                        state.clay_robots,
                        state.obsidian_robots,
                        state.geode_robots,
                    ),
                )
            )

        # wait to buy a new clay-collecting robot
        time_to_clay_robot = max(ceil((blueprint.clay_robot_cost_ore - state.ore) / state.ore_robots) + 1, 1)
        if time + time_to_clay_robot <= max_time and state.clay_robots < blueprint.obsidian_robot_cost_clay:
            open_set.append(
                (
                    time + time_to_clay_robot,
                    State(
                        state.ore + state.ore_robots * time_to_clay_robot - blueprint.clay_robot_cost_ore,
                        state.clay + state.clay_robots * time_to_clay_robot,
                        state.obsidian + state.obsidian_robots * time_to_clay_robot,
                        state.geodes + state.geode_robots * time_to_clay_robot,
                        state.ore_robots,
                        state.clay_robots + 1,
                        state.obsidian_robots,
                        state.geode_robots,
                    ),
                )
            )

        # wait to buy a new obsidian-collecting robot
        if state.clay_robots >= 1 and state.obsidian_robots < blueprint.geode_robot_cost_obsidian:
            time_to_obsidian_robot = max(
                ceil((blueprint.obsidian_robot_cost_ore - state.ore) / state.ore_robots) + 1,
                ceil((blueprint.obsidian_robot_cost_clay - state.clay) / state.clay_robots) + 1,
                1,
            )
            if time + time_to_obsidian_robot <= max_time:
                open_set.append(
                    (
                        time + time_to_obsidian_robot,
                        State(
                            state.ore + state.ore_robots * time_to_obsidian_robot - blueprint.obsidian_robot_cost_ore,
                            state.clay
                            + state.clay_robots * time_to_obsidian_robot
                            - blueprint.obsidian_robot_cost_clay,
                            state.obsidian + state.obsidian_robots * time_to_obsidian_robot,
                            state.geodes + state.geode_robots * time_to_obsidian_robot,
                            state.ore_robots,
                            state.clay_robots,
                            state.obsidian_robots + 1,
                            state.geode_robots,
                        ),
                    )
                )

        # wait to buy a geode robot
        if state.obsidian_robots > 0:
            time_to_geode_robot = max(
                ceil((blueprint.geode_robot_cost_ore - state.ore) / state.ore_robots) + 1,
                ceil((blueprint.geode_robot_cost_obsidian - state.obsidian) / state.obsidian_robots) + 1,
                1,
            )
            if time + time_to_geode_robot <= max_time:
                open_set.append(
                    (
                        time + time_to_geode_robot,
                        State(
                            state.ore + state.ore_robots * time_to_geode_robot - blueprint.geode_robot_cost_ore,
                            state.clay + state.clay_robots * time_to_geode_robot,
                            state.obsidian
                            + state.obsidian_robots * time_to_geode_robot
                            - blueprint.geode_robot_cost_obsidian,
                            state.geodes + state.geode_robots * time_to_geode_robot,
                            state.ore_robots,
                            state.clay_robots,
                            state.obsidian_robots,
                            state.geode_robots + 1,
                        ),
                    )
                )
    return most_geodes


def problem_1() -> None:
    blueprints = [Blueprint(*islice(map(int, re.findall(r"\d+", line)), 1, None)) for line in lines]
    print(sum(most_geodes_for_blueprint(blueprint, 24) * i for i, blueprint in enumerate(blueprints, start=1)))


def problem_2() -> None:
    blueprints = [Blueprint(*islice(map(int, re.findall(r"\d+", line)), 1, None)) for line in lines[:3]]
    print(prod(most_geodes_for_blueprint(blueprint, 32) for blueprint in blueprints))
