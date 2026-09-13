import ast
from collections import Counter, deque
from fractions import Fraction
from itertools import product
from math import ceil, floor

import numpy as np

with open("./2025/resources/10.txt") as f:
    lines = f.read().splitlines()


def part_1() -> None:
    total = 0
    for line in lines:
        desired = {i for i, c in enumerate(line[1 : line.index("]")]) if c == "#"}
        buttons = [
            (ast.literal_eval(tup[:-1] + "," + ")")) for tup in line[line.index("(") : line.rindex(")") + 1].split()
        ]
        # each button toggles the state its lights, so it should be either not pressed or pressed only once
        # sort by total presses so that we can stop on the first success
        for button_presses in sorted(product((False, True), repeat=len(buttons)), key=sum):
            counter = Counter[int]()
            for include, b in zip(button_presses, buttons):
                if include:
                    counter.update(b)
            lights_on = {pos for pos, val in counter.items() if val % 2 == 1}
            if lights_on == desired:
                total += sum(button_presses)
                break
    print(total)


def part_2() -> None:
    type Constraint = tuple[int, int]

    def run_simplex(tableau: np.ndarray, basis_columns: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        # Run the simplex algorithm for min Z. The first row is the objective function, and the last column is the RHS.
        # Make the Z row consistent with the table
        for i, col in enumerate(basis_columns):
            if tableau[0, col] != 0:
                tableau[0, :] += tableau[i + 1, :]

        while True:
            if (tableau[0, :-1] <= 0).all():  # finished
                return tableau, basis_columns
            pivot_col = tableau[0, :-1].argmax()
            nonzero_entries = np.where(tableau[1:, pivot_col] > 0)[0] + 1
            pivot_row = nonzero_entries[(tableau[nonzero_entries, -1] / tableau[nonzero_entries, pivot_col]).argmin()]
            basis_columns[pivot_row - 1] = pivot_col
            tableau[pivot_row, :] /= tableau[pivot_row, pivot_col]
            for i in range(tableau.shape[0]):  # pivot
                if i == pivot_row:
                    continue
                if (factor := tableau[i, pivot_col]) == 0:
                    continue
                tableau[i, :] -= factor * tableau[pivot_row, :]

    def solve_lp_problem(
        A: np.ndarray, b: np.ndarray, le_constraints: list[Constraint], ge_constraints: list[Constraint]
    ) -> tuple[np.ndarray, Fraction] | None:
        # Two phase simplex method, largely from
        # https://uomustansiriyah.edu.iq/media/lectures/6/6_2022_01_08!08_05_56_PM.pdf
        # Phase I: find a basic feasible solution to run the simplex method on.
        m, n = A.shape  # m constraints, n variables
        # Add slack variables for any inequality constraints
        n_slack = len(le_constraints) + len(ge_constraints)
        slack_constraints = np.zeros((n_slack, n + n_slack), dtype=int)
        rhs_slack_variables = np.zeros(n_slack, dtype=int)
        for i, (idx, constraint) in enumerate(le_constraints):
            slack_constraints[i, idx] = 1
            slack_constraints[i, n + i] = 1
            rhs_slack_variables[i] = constraint
        for j, (idx, constraint) in enumerate(ge_constraints, start=len(le_constraints)):
            slack_constraints[j, idx] = 1
            slack_constraints[j, n + j] = -1
            rhs_slack_variables[j] = constraint

        # Add artificial variables to any rows which do not already have a basis
        real_variables_tableau = np.block([[A, np.zeros((m, n_slack), int)], [slack_constraints]])
        basis_columns = np.where(real_variables_tableau.sum(axis=0) == 1)[0]
        rows_needing_basis = np.where(real_variables_tableau[:, basis_columns].sum(axis=1) == 0)[0]
        n_artificial = rows_needing_basis.size
        # The tableau columns are original variables, then slack variables, then artificial variables, then the RHS
        # For phase 1, the objective is min Z = sum(artificial variables)
        tableau = np.block(
            [
                [np.zeros((1, n + n_slack), int), -np.ones((1, n_artificial), int), 0],
                [A, np.zeros((m, n_slack + n_artificial), int), b.reshape((m, 1))],
                [slack_constraints, np.zeros((n_slack, n_artificial), int), rhs_slack_variables.reshape((n_slack, 1))],
            ]
        )

        # Basis holds the index of the current basis column for each row
        basis = np.zeros(m + n_slack, dtype=int)
        basis[real_variables_tableau[:, basis_columns].argmax(axis=0)] = basis_columns
        for i, j in enumerate(rows_needing_basis):
            tableau[j + 1, n + n_slack + i] = 1
            basis[j] = n + n_slack + i
        # Convert to fractions for exact arithmetic
        tableau = tableau + Fraction()

        tableau, basis = run_simplex(tableau, basis)

        # Check which of the three cases the phase I solution resulted in
        phase_1_objective_value = tableau[0, -1]
        if phase_1_objective_value > 0:
            # Case 1, LP problem has no feasible solution
            return None
        if (basis < n + n_slack).all():
            # Case 2, no artificial variables remain in the basis. Drop all the artificial variables.
            tableau = np.block([tableau[:, : n + n_slack], tableau[:, -1].reshape(m + n_slack + 1, 1)])
        else:
            # Case 3, artificial variables remain in the basis; pivot in non-artificial variables (real or slack)
            artificial_basis_rows = np.where(basis >= n + n_slack)[0] + 1
            rows_to_keep = np.ones(1 + m + n_slack, bool)
            for pivot_row in artificial_basis_rows:
                row = tableau[pivot_row, : n + n_slack]
                if (row == 0).all():
                    # No non-artificial pivots are available, so the row is redundant; drop it
                    rows_to_keep[pivot_row] = 0
                    continue
                # Otherwise, pivot
                pivot_col = (row != 0).argmax()
                tableau[pivot_row, :] /= tableau[pivot_row, pivot_col]
                for i in range(tableau.shape[0]):
                    if i == pivot_row:
                        continue
                    if (factor := tableau[i, pivot_col]) == 0:
                        continue
                    tableau[i, :] -= factor * tableau[pivot_row, :]
                basis[pivot_row - 1] = pivot_col
            basis = basis[rows_to_keep[1:]]
            tableau = np.block([tableau[rows_to_keep, : n + n_slack], tableau[rows_to_keep, -1].reshape((-1, 1))])

        # Restore the original objective function for Phase II
        tableau[0, :n] = Fraction(-1)
        tableau[0, n:] = Fraction(0)

        tableau, basis = run_simplex(tableau, basis)

        final_values = np.full(n + n_slack, Fraction(0), dtype=object)
        final_values[basis] = tableau[1:, -1]
        return final_values[:n], tableau[0, -1]

    total = 0
    for line in lines:
        b = np.array([int(x) for x in line[line.index("{") + 1 : -1].split(",")])
        buttons: list[set[int]] = [
            set(ast.literal_eval(tup[:-1] + "," + ")")) for tup in line[line.index("(") : line.rindex(")") + 1].split()
        ]
        n = len(buttons)
        m = b.shape[0]
        A = np.zeros((m, n), int)
        for col, button in enumerate(buttons):
            for i in range(m):
                if i in button:
                    A[i, col] = 1

        # If we can solve any problems directly or via least-squares, do that, as it is faster than the ILP solver
        if m == n and np.linalg.det(A) >= 1e-3:
            total += round(np.linalg.solve(A, b).sum())
            continue
        if abs(np.linalg.det(A.T @ A)) >= 1e-3:
            total += round(np.linalg.solve(A.T @ A, A.T @ b).sum())
            continue

        # Branch and bound algorithm
        active_problems: deque[tuple[list[Constraint], list[Constraint]]] = deque([([], [])])
        best_objective_value = float("inf")
        while active_problems:
            le_constraints, ge_constraints = active_problems.popleft()
            solution = solve_lp_problem(A, b, le_constraints, ge_constraints)
            if solution is None:
                continue
            x, objective_value = solution
            if ceil(objective_value) >= best_objective_value:
                continue
            if all(xi.is_integer() for xi in x):
                best_objective_value = objective_value
                continue
            # non-integer solutions: most infeasible branching
            i = np.minimum(x - np.floor(x), np.ceil(x) - x).argmax()
            floor_xi = floor(x[i])
            ceil_xi = ceil(x[i])
            existing_index = next((i for i, constraint in enumerate(le_constraints) if constraint[0] == i), None)
            if existing_index is None:
                new_le_constraints = le_constraints + [(i, floor_xi)]
            else:
                new_le_constraints = le_constraints.copy()
                new_le_constraints[existing_index] = (i, min(floor_xi, new_le_constraints[existing_index][1]))
            existing_index = next((i for i, constraint in enumerate(ge_constraints) if constraint[0] == i), None)
            if existing_index is None:
                new_ge_constraints = ge_constraints + [(i, ceil_xi)]
            else:
                new_ge_constraints = ge_constraints.copy()
                new_ge_constraints[existing_index] = (i, max(ceil_xi, new_ge_constraints[existing_index][1]))

            active_problems.append((new_le_constraints, ge_constraints))
            active_problems.append((le_constraints, new_ge_constraints))

        total += round(best_objective_value)

    print(total)
