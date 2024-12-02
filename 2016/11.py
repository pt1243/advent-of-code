from collections import namedtuple
from itertools import chain, combinations
import heapq
from typing import cast


with open("./2016/resources/11.txt") as f:
    lines = f.read().splitlines()


def find_min_steps(lines: list[str], extra_first_floor_elements: list[str] | None = None) -> int:
    if extra_first_floor_elements is None:
        extra_first_floor_elements = []

    microchip_starting_floors = {}
    generator_starting_floors = {}
    for floor, line in enumerate(lines, start=1):
        if "nothing relevant" in line:
            continue
        line = line[line.index("contains") + 9 : -1]
        if "," in line:
            items = line.split(", ")
        else:
            items = line.split(" and a ")
        for item in items:
            item = item.lstrip("and ").lstrip("a ")
            if "generator" in item:
                generator_starting_floors[item.split()[0]] = floor
            else:
                microchip_starting_floors[item[: item.index("-")]] = floor

    for element in extra_first_floor_elements:
        microchip_starting_floors[element] = 1
        generator_starting_floors[element] = 1

    num_elements = len(microchip_starting_floors)
    kwargs = {
        "steps": 0,
        "distance_to_top_floor": 2 * num_elements * 4
        - sum(microchip_starting_floors.values())
        - sum(generator_starting_floors.values()),
        "elevator_position": 1,
    }
    for element, microchip_starting_floor in microchip_starting_floors.items():
        kwargs[f"{element}_microchip"] = microchip_starting_floor
        kwargs[f"{element}_generator"] = generator_starting_floors[element]

    # unsurprisingly, mypy is not particularly happy about a dynamically created type
    State = namedtuple("State", kwargs.keys())  # type: ignore[misc]

    def deduplicate_state(state: State) -> State:
        return State(
            *chain(
                state[:3],
                chain.from_iterable(sorted([(state[2 * i + 3], state[2 * i + 4]) for i in range(num_elements)])),
            )
        )

    possible_states = [deduplicate_state(State(**kwargs))]
    states_to_check = {possible_states[0]}
    while True:
        state = heapq.heappop(possible_states)
        states_to_check.remove(state)

        microchips: list[str] = list(state[3::2])
        generators: list[str] = list(state[4::2])

        # check that the state is valid
        valid = True
        for i in range(num_elements):
            microchip_floor = microchips[i]
            if microchip_floor != generators[i] and any(
                microchip_floor == generator_floor for generator_floor in generators[:i] + generators[i + 1 :]
            ):
                valid = False
                break
        if not valid:
            continue

        if state.distance_to_top_floor == 0:  # type: ignore[attr-defined]
            return cast(int, state.steps)  # type: ignore[attr-defined]

        # find possible new states
        current_floor_items = [i for i in range(3, 3 + 2 * num_elements) if state[i] == state.elevator_position]  # type: ignore[attr-defined]
        # first, all possible states that take one item from the current floor
        for i in current_floor_items:
            replacement_args = {
                "steps": state.steps + 1,  # type: ignore[attr-defined]
                "distance_to_top_floor": state.distance_to_top_floor + 1,  # type: ignore[attr-defined]
                "elevator_position": state.elevator_position - 1,  # type: ignore[attr-defined]
                state._fields[i]: state[i] - 1,
            }
            if state.elevator_position > 1:  # type: ignore[attr-defined]
                new_state = deduplicate_state(state._replace(**replacement_args))
                if new_state not in states_to_check:
                    states_to_check.add(new_state)
                    heapq.heappush(possible_states, new_state)

            if state.elevator_position < 4:  # type: ignore[attr-defined]
                replacement_args["elevator_position"] = state.elevator_position + 1  # type: ignore[attr-defined]
                replacement_args["distance_to_top_floor"] = state.distance_to_top_floor - 1  # type: ignore[attr-defined]
                replacement_args[state._fields[i]] = state[i] + 1
                new_state = deduplicate_state(state._replace(**replacement_args))
                if new_state not in states_to_check:
                    states_to_check.add(new_state)
                    heapq.heappush(possible_states, new_state)

        # two items from the current floor:
        for i, j in combinations(current_floor_items, 2):
            replacement_args = {
                "steps": state.steps + 1,  # type: ignore[attr-defined]
                "distance_to_top_floor": state.distance_to_top_floor + 2,  # type: ignore[attr-defined]
                "elevator_position": state.elevator_position - 1,  # type: ignore[attr-defined]
                state._fields[i]: state[i] - 1,
                state._fields[j]: state[j] - 1,
            }
            if state.elevator_position > 1:  # type: ignore[attr-defined]
                new_state = deduplicate_state(state._replace(**replacement_args))
                if new_state not in states_to_check:
                    states_to_check.add(new_state)
                    heapq.heappush(possible_states, new_state)
            if state.elevator_position < 4:  # type: ignore[attr-defined]
                replacement_args["distance_to_top_floor"] = state.distance_to_top_floor - 2  # type: ignore[attr-defined]
                replacement_args["elevator_position"] = state.elevator_position + 1  # type: ignore[attr-defined]
                replacement_args[state._fields[i]] = state[i] + 1
                replacement_args[state._fields[j]] = state[j] + 1
                new_state = deduplicate_state(state._replace(**replacement_args))
                if new_state not in states_to_check:
                    states_to_check.add(new_state)
                    heapq.heappush(possible_states, new_state)


def problem_1() -> None:
    print(find_min_steps(lines))


def problem_2() -> None:
    print(find_min_steps(lines, extra_first_floor_elements=["elerium", "dilithium"]))
