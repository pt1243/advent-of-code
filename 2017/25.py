from collections import defaultdict
from typing import NamedTuple


blueprint = """\
Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A."""

with open("./2017/resources/25.txt") as f:
    blueprint = f.read().strip()


class State(NamedTuple):
    current_0_write: int
    current_0_move: int
    current_0_next: str
    current_1_write: int
    current_1_move: int
    current_1_next: str


def problem_1() -> None:
    blueprint_states = blueprint.split("\n\n")
    header = blueprint_states[0].split("\n")
    starting_state = header[0].split()[-1][0]
    steps = int(header[1].split()[-2])

    states: dict[str, State] = {}
    for state_string in blueprint_states[1:]:
        lines = state_string.split("\n")
        states[lines[0].split()[-1][0]] = State(
            int(lines[2].split()[-1][0]),
            -1 if lines[3].split()[-1][:-1] == "left" else 1,
            lines[4].split()[-1][0],
            int(lines[6].split()[-1][0]),
            -1 if lines[7].split()[-1][:-1] == "left" else 1,
            lines[8].split()[-1][0],
        )

    position = 0
    tape: defaultdict[int, int] = defaultdict(int)
    state = states[starting_state]
    for _ in range(steps):
        if not tape[position]:
            tape[position] = state.current_0_write
            position += state.current_0_move
            state = states[state.current_0_next]
        else:
            tape[position] = state.current_1_write
            position += state.current_1_move
            state = states[state.current_1_next]
    print(sum(tape.values()))
