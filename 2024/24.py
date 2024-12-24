from __future__ import annotations
from collections.abc import Sequence
from functools import cache
from operator import xor, or_, and_
from typing import ClassVar


with open("./2024/resources/24.txt") as f:
    text = f.read().strip()


class Gate:
    input_values: ClassVar[dict[str, int]] = {}
    lookup: ClassVar[dict[str, Gate]] = {}

    def __init__(self, line: str):
        left, name = line.split(" -> ")
        self.name = name
        type(self).lookup[name] = self
        arg_1, op, arg_2 = left.split()
        self.arg_1 = arg_1
        self.arg_2 = arg_2
        self.op = {"AND": and_, "XOR": xor, "OR": or_}[op]

    @cache
    def evaluate(self) -> int:
        return self.op(self.resolve(self.arg_1), self.resolve(self.arg_2))

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

    # manually found
    Gate.swap("ggt", "mwh")
    Gate.swap("z06", "fhc")
    Gate.swap("qhj", "z11")
    Gate.swap("z35", "hqk")

    # NOTE: if there are two sequential numbers with problems (ie. 5 and 6, 10 and 11, 34 and 35), the fix needs to
    # involve both; based on the manually found solutions, this suggests that the upper z output should be one of the
    # swapped gates. Not sure if this is universal or if it just happens to work for this specific case.

    print(",".join(sorted(["ggt", "mwh", "z06", "fhc", "qhj", "z11", "z35", "hqk"])))

    zeros = [0] * 45
    for bit_position in range(45):
        x = zeros.copy()
        y = zeros.copy()
        x[44 - bit_position] = 1
        y[44 - bit_position] = 1

        result_both = Gate.add_values(x, y)
        result_x_only = Gate.add_values(x, zeros)
        result_y_only = Gate.add_values(zeros, y)

        wrong_both = result_both != 2 ** (bit_position + 1)
        wrong_x_only = result_x_only != 2**bit_position
        wrong_y_only = result_y_only != 2**bit_position

        if wrong_both:
            print(
                f"Erroneous result for 1 AND 1 on {bit_position = }: output should be {2 ** (bit_position + 1)} but is {result_both}"
            )
        if wrong_x_only:
            print(
                f"Erroneous result for x only on {bit_position = }: output should be {2 ** bit_position} but is {result_x_only}"
            )
        if wrong_y_only:
            print(
                f"Erroneous result for y only on {bit_position = }: output should be {2 ** bit_position} but is {result_y_only}"
            )

        if any((wrong_both, wrong_x_only, wrong_y_only)):  # easier to read
            print()
