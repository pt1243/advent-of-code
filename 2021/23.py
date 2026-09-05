import heapq
from collections import defaultdict
from collections.abc import Iterable
from enum import IntEnum
from typing import NamedTuple, cast

with open("./2021/resources/23.txt") as f:
    lines = f.read().splitlines()


def calculate_cost(starting_rows: Iterable[Iterable[str]]) -> int:
    class Amphipod(IntEnum):
        A = 0
        B = 1
        C = 2
        D = 3

    class Location(IntEnum):
        HallwayLeftEnd = 4
        HallwayLeft = 5
        AB = 6
        BC = 7
        CD = 8
        HallwayRight = 9
        HallwayRightEnd = 10

    class State(NamedTuple):
        a_stack: tuple[Amphipod, ...]
        b_stack: tuple[Amphipod, ...]
        c_stack: tuple[Amphipod, ...]
        d_stack: tuple[Amphipod, ...]
        HallwayLeftEnd: Amphipod | None = None
        HallwayLeft: Amphipod | None = None
        AB: Amphipod | None = None
        BC: Amphipod | None = None
        CD: Amphipod | None = None
        HallwayRight: Amphipod | None = None
        HallwayRightEnd: Amphipod | None = None

        def is_final_state(self) -> bool:
            return (
                self.a_stack == (Amphipod.A,) * stack_size
                and self.b_stack == (Amphipod.B,) * stack_size
                and self.c_stack == (Amphipod.C,) * stack_size
                and self.d_stack == (Amphipod.D,) * stack_size
            )

        # this is safe but ty/mypy don't understand that we are comparing compatible types here
        def __lt__(self, value: State) -> bool:  # ty: ignore[invalid-method-override]
            return self[:4] < value[:4]  # ty: ignore[unsupported-operator]

    distances_and_paths = (
        {
            Location.HallwayLeftEnd: (3, (Location.HallwayLeft,)),
            Location.HallwayLeft: (2, ()),
            Location.AB: (2, ()),
            Location.BC: (4, (Location.AB,)),
            Location.CD: (6, (Location.AB, Location.BC)),
            Location.HallwayRight: (8, (Location.AB, Location.BC, Location.CD)),
            Location.HallwayRightEnd: (9, (Location.AB, Location.BC, Location.CD, Location.HallwayRight)),
        },
        {
            Location.HallwayLeftEnd: (5, (Location.AB, Location.HallwayLeft)),
            Location.HallwayLeft: (4, (Location.AB,)),
            Location.AB: (2, ()),
            Location.BC: (2, ()),
            Location.CD: (4, (Location.BC,)),
            Location.HallwayRight: (6, (Location.BC, Location.CD)),
            Location.HallwayRightEnd: (7, (Location.BC, Location.CD, Location.HallwayRight)),
        },
        {
            Location.HallwayLeftEnd: (7, (Location.BC, Location.AB, Location.HallwayLeft)),
            Location.HallwayLeft: (6, (Location.BC, Location.AB)),
            Location.AB: (4, (Location.BC,)),
            Location.BC: (2, ()),
            Location.CD: (2, ()),
            Location.HallwayRight: (4, (Location.CD,)),
            Location.HallwayRightEnd: (5, (Location.CD, Location.HallwayRight)),
        },
        {
            Location.HallwayLeftEnd: (9, (Location.CD, Location.BC, Location.AB, Location.HallwayLeft)),
            Location.HallwayLeft: (8, (Location.CD, Location.BC, Location.AB)),
            Location.AB: (6, (Location.CD, Location.BC)),
            Location.BC: (4, (Location.CD,)),
            Location.CD: (2, ()),
            Location.HallwayRight: (2, ()),
            Location.HallwayRightEnd: (3, (Location.HallwayRight,)),
        },
    )

    # ty does not understand we aren't passing inputs to the hallway positions here
    initial_state = State(*(tuple(Amphipod[char] for char in stack) for stack in zip(*starting_rows)))  # ty: ignore[invalid-argument-type]
    stack_size = len(initial_state.a_stack)

    g_score = defaultdict[State, int](lambda: 10**12)
    g_score[initial_state] = 0
    open_set = [(0, initial_state)]
    while open_set:
        _, current = heapq.heappop(open_set)
        current_g_score = g_score[current]
        if current.is_final_state():
            return current_g_score
        candidate_neighbours_and_costs: list[tuple[State, int]] = []
        # try moving out of rooms into the hallway; note that even a direct move to another room always goes through a
        # hallway position
        for stack_idx in range(4):
            stack = cast(tuple[Amphipod, ...], current[stack_idx])
            # move top of stack to hallway
            if not stack:
                continue
            tos = stack[-1]
            if tos != stack_idx or any(amphipod != stack_idx for amphipod in stack[:-1]):
                for hallway_location in Location:
                    if current[hallway_location] is None:
                        distance, path = distances_and_paths[stack_idx][hallway_location]
                        if all(current[intermediate] is None for intermediate in path):
                            candidate_neighbours_and_costs.append(
                                (
                                    current._make(
                                        (
                                            *current[:stack_idx],
                                            stack[:-1],
                                            *current[stack_idx + 1 : hallway_location],
                                            tos,
                                            *current[hallway_location + 1 :],
                                        )
                                    ),
                                    (distance + stack_size - len(stack)) * 10**tos,
                                )
                            )
        # move from hallway to room
        for hallway_location in Location:
            if current[hallway_location.value] is None:
                continue
            amphipod = cast(Amphipod, current[hallway_location.value])
            stack = cast(tuple[Amphipod, ...], current[amphipod])
            if all(amphipod_in_stack == amphipod for amphipod_in_stack in stack):
                distance, path = distances_and_paths[amphipod][hallway_location]
                if all(current[intermediate] is None for intermediate in path):
                    candidate_neighbours_and_costs.append(
                        (
                            current._make(
                                (
                                    *current[:amphipod],
                                    stack + (amphipod,),
                                    *current[amphipod + 1 : hallway_location],
                                    None,
                                    *current[hallway_location + 1 :],
                                )
                            ),
                            (distance + stack_size - 1 - len(stack)) * 10**amphipod,
                        )
                    )
        for neighbour, cost in candidate_neighbours_and_costs:
            tentative_g_score = current_g_score + cost
            if tentative_g_score < g_score[neighbour]:
                g_score[neighbour] = tentative_g_score
                heapq.heappush(open_set, (tentative_g_score, neighbour))
    raise ValueError("did not find solution")


def part_1() -> None:
    starting_rows = (lines[3][3:10:2], lines[2][3:10:2])
    print(calculate_cost(starting_rows))


def part_2() -> None:
    starting_rows = (lines[3][3:10:2], "DBAC", "DCBA", lines[2][3:10:2])
    print(calculate_cost(starting_rows))
