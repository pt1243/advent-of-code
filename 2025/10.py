import ast
from collections import Counter
from itertools import product
from typing import cast

import numpy as np
import scipy.optimize

with open("./2025/resources/10.txt") as f:
    lines = f.read().splitlines()


def part_1() -> None:
    total = 0
    for line in lines:
        desired = set(i for i, c in enumerate(line[1 : line.index("]")]) if c == "#")
        buttons = [
            (ast.literal_eval(tup[:-1] + "," + ")")) for tup in line[line.index("(") : line.rindex(")") + 1].split()
        ]
        # each button toggles the state its lights, so it should be either not pressed or pressed only once
        # sort by total presses so that we can stop on the first success
        for button_presses in sorted(product((False, True), repeat=len(buttons)), key=sum):
            counter: Counter[int] = Counter()
            for include, b in zip(button_presses, buttons):
                if include:
                    counter.update(b)
            lights_on = set(pos for pos, val in counter.items() if val % 2 == 1)
            if lights_on == desired:
                total += sum(button_presses)
                break
    print(total)


def part_2() -> None:
    total = 0
    for line in lines:
        desired = tuple(map(int, line[line.index("{") + 1 : -1].split(",")))
        buttons: list[set[int]] = [
            set(ast.literal_eval(tup[:-1] + "," + ")")) for tup in line[line.index("(") : line.rindex(")") + 1].split()
        ]

        # minimize c^T x
        # subject to:
        #   all x are integral (integrality)
        #   x >= 0 (bounds)
        #   desired <= A @ x <= desired (constraints)
        # x is the number of times each button is pressed, c is a vector of ones, and the columns of A are whether each
        # index is affected by that button or not
        variable_size = len(buttons)
        constraint_size = len(desired)
        c = np.ones(variable_size, int)
        A = np.zeros((constraint_size, variable_size), int)
        for col, button in enumerate(buttons):
            for i in range(constraint_size):
                if i in button:
                    A[i, col] = 1

        sol = scipy.optimize.milp(
            c,
            integrality=np.ones(variable_size, int),
            bounds=scipy.optimize.Bounds(0),  # type: ignore[arg-type]  # unsure why mypy doesn't like this
            constraints=scipy.optimize.LinearConstraint(A, desired, desired),
        )
        total += int(cast(int, sol.fun))
    print(total)
