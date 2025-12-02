from __future__ import annotations

from collections import defaultdict
from collections.abc import Sequence
from functools import cache
from itertools import combinations
from operator import and_, or_, xor
from typing import ClassVar, cast

with open("./2024/resources/24.txt") as f:
    text = f.read().strip()


class Gate:
    input_values: ClassVar[dict[str, int]] = {}
    lookup: ClassVar[dict[str, Gate]] = {}
    associated_gates: ClassVar[defaultdict[str, set[str]]] = defaultdict(set)

    def __init__(self, line: str):
        left, name = line.split(" -> ")
        self.name = name
        type(self).lookup[name] = self
        arg_1, op, arg_2 = left.split()
        self.arg_1 = arg_1
        self.arg_2 = arg_2
        type(self).associated_gates[name].add(arg_1)
        type(self).associated_gates[name].add(arg_2)
        type(self).associated_gates[arg_1].add(name)
        type(self).associated_gates[arg_2].add(name)
        self.op = {"AND": and_, "XOR": xor, "OR": or_}[op]

    @cache
    def evaluate(self) -> int:
        return cast(int, self.op(self.resolve(self.arg_1), self.resolve(self.arg_2)))

    @classmethod
    def resolve(cls, arg: str) -> int:
        if arg in cls.input_values:
            return cls.input_values[arg]
        return cls.lookup[arg].evaluate()

    @classmethod
    def swap(cls, name_1: str, name_2: str) -> None:
        gate_1 = cls.lookup[name_1]
        gate_2 = cls.lookup[name_2]
        gate_1.name, gate_2.name = gate_2.name, gate_1.name
        cls.lookup[name_1] = gate_2
        cls.lookup[name_2] = gate_1

    @classmethod
    def add_values(cls, x: Sequence[int], y: Sequence[int]) -> int:
        for i, bit in enumerate(reversed(x)):
            cls.input_values[f"x{str(i).zfill(2)}"] = bit
        for i, bit in enumerate(reversed(y)):
            cls.input_values[f"y{str(i).zfill(2)}"] = bit

        for gate in cls.lookup.values():
            gate.evaluate.cache_clear()

        z_wires: list[tuple[str, int]] = []
        for gate in cls.lookup.values():
            result = gate.evaluate()
            if gate.name.startswith("z"):
                z_wires.append((gate.name, result))
        return int("".join(str(z[1]) for z in sorted(z_wires, reverse=True)), 2)


def problem_1() -> None:
    input_wire_lines, gate_lines = text.split("\n\n")
    x_bits: list[tuple[str, str]] = []
    y_bits: list[tuple[str, str]] = []
    for line in input_wire_lines.split("\n"):
        name, value = line.split(": ")
        if name.startswith("x"):
            x_bits.append((name, value))
        else:
            y_bits.append((name, value))
    x = list(int(x[1]) for x in sorted(x_bits, reverse=True))
    y = list(int(y[1]) for y in sorted(y_bits, reverse=True))

    for line in gate_lines.split("\n"):
        Gate(line)

    print(Gate.add_values(x, y))


def problem_2() -> None:
    gate_lines = text.split("\n\n")[1]
    for line in gate_lines.split("\n"):
        Gate(line)

    zeros = [0] * 45

    def wrong_value(bit_position: int) -> bool:
        x = zeros.copy()
        y = zeros.copy()
        x[44 - bit_position] = 1
        y[44 - bit_position] = 1

        try:
            result_both = Gate.add_values(x, y)
            result_x_only = Gate.add_values(x, zeros)
            result_y_only = Gate.add_values(zeros, y)
        except RecursionError:  # hacky way to detect cycles
            return True

        wrong_both = result_both != 2 ** (bit_position + 1)
        wrong_x_only = result_x_only != 2**bit_position
        wrong_y_only = result_y_only != 2**bit_position

        return any((wrong_both, wrong_x_only, wrong_y_only))

    # NOTE: if there are two sequential numbers with problems (ie. 5 and 6, 10 and 11, 34 and 35), the fix needs to
    # involve both; based on the manually found solutions, this suggests that the upper z output should be one of the
    # swapped gates. Not sure if this is universal or if it just happens to work for this specific case.
    swapped_gates = []

    for i in range(45):
        if wrong_value(i):
            current_gate_string = str(i).zfill(2)
            current_x = f"x{current_gate_string}"
            current_y = f"y{current_gate_string}"
            current_z = f"z{current_gate_string}"
            starting_point = {current_x, current_y, current_z}

            consider_both_values = wrong_value(i + 1)
            if consider_both_values:  # whether the next bit is also wrong
                next_gate_string = str(i + 1).zfill(2)
                next_x = f"x{next_gate_string}"
                next_y = f"y{next_gate_string}"
                next_z = f"z{next_gate_string}"
                starting_point |= {next_x, next_y, next_z}

            first_degree = set().union(*(Gate.associated_gates[gate] for gate in starting_point))
            second_degree = (
                set().union(*(Gate.associated_gates[gate] for gate in first_degree)) | starting_point | first_degree
            )

            second_degree -= {current_x, current_y}
            if consider_both_values:
                second_degree -= {next_x, next_y}

            for gate_1, gate_2 in combinations(second_degree, 2):
                # it seems that if the next bit is also wrong, the swap needs to involve the output of the next bit
                if consider_both_values:
                    if next_z != gate_1 and next_z != gate_2:
                        continue
                Gate.swap(gate_1, gate_2)
                if not (wrong_value(i - 1) or wrong_value(i) or wrong_value(i + 1)):  # successful swap
                    swapped_gates.append(gate_1)
                    swapped_gates.append(gate_2)
                    break
                Gate.swap(gate_1, gate_2)  # otherwise, undo the swap

    print(",".join(sorted(swapped_gates)))
