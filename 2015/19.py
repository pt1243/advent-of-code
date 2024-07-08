from collections import defaultdict
from collections.abc import Iterable
from itertools import count

from pprint import pprint

from more_itertools import split_before
import numpy as np


with open('./2015/resources/19.txt') as f:
    lines = [line.strip() for line in f]

class CNFGrammar:
    def __init__(self, initial_rules: Iterable[tuple[str, str]], final: str):
        self.final = final
        self.rules: defaultdict[str, set[tuple[str, ...]]] = defaultdict(set)
        for lhs, rhs in initial_rules:
            self.rules[lhs].add(tuple("".join(x) for x in split_before(rhs, lambda s: s.isupper())))
        
        final_symbols = ("".join(x) for x in split_before(final, lambda s: s.isupper()))
        for s in final_symbols:
            self.rules[s].add((f"TERM_{s}",))
        self.terminals = {term for options in self.rules.values() for rhs in options for term in rhs if term not in self.rules.keys()}
        self.terminals.update(f"TERM_{s}" for s in final_symbols)
        pprint(self.terminals)

        # print("before starting")
        # pprint(self.rules)

        self._run_term()
        # print("after TERM")
        # pprint(self.rules)
        self._run_bin()
        # print("after BIN")
        # pprint(self.rules)
        # self._run_del()
        self._run_unit()
        # print("after UNIT")
        # pprint(self.rules)

    def _run_term(self):
        new_rules: defaultdict[str, set[tuple[str, ...]]] = defaultdict(set)

        for lhs, options in self.rules.items():
            for rhs in options:
                terminals_present = [t for t in rhs if t in self.terminals]
                if len(rhs) > len(terminals_present):
                    for t in terminals_present:
                        new_rules[f"N_{t}"].add(t)
                    new_rhs = [orig if orig not in self.terminals else f"N_{orig}" for orig in rhs]
                    new_rules[lhs].add(tuple(new_rhs))
                else:
                    new_rules[lhs].add(rhs)
        self.rules = new_rules

    def _run_bin(self):
        new_rules: defaultdict[str, set[tuple[str, ...]]] = defaultdict(set)
        for lhs, options in self.rules.items():
            for rhs in options:
                if len(rhs) > 2:
                    new_rules[lhs].add((rhs[0], f"{lhs}_1"))
                    for n in range(1, len(rhs) - 2):
                        new_rules[f"{lhs}_{n}"].add((rhs[n], f"{lhs}_{n+1}"))
                    new_rules[f"{lhs}_{len(rhs) - 2}"].add((rhs[-2], rhs[-1]))
                else:
                    new_rules[lhs].add(rhs)

        self.rules = new_rules
        # pprint(self.rules)

    def _run_del(self):
        pass  # no epsilon rules

    def _run_unit(self):
        new_rules: defaultdict[str, set[tuple[str, ...]]] = defaultdict(set)
        # pprint(self.rules)
        for lhs, options in self.rules.items():
            for rhs in options:
                if len(rhs) == 1 and lhs not in self.terminals and rhs[0] not in self.terminals:
                    new_rules[lhs].update(self.rules[rhs[0]])
                else:
                    new_rules[lhs].add(rhs)
        
        self.rules = new_rules
        # pprint(self.rules)
    
    def CYK(self):
        # pprint(self.rules)
        target_symbols = ["TERM_" + "".join(x) for x in split_before(self.final, lambda s: s.isupper())]
        counter = count(1)
        R_index = {}
        R_index["e"] = 0
        for sym in self.rules.keys():
            if sym in self.terminals:
                continue
            if sym == "e":
                continue
            R_index[sym] = next(counter)
        pprint(R_index)
        n = len(target_symbols)
        r = len(R_index)
        P = np.zeros((n, n, r), dtype=bool)
        back = defaultdict(list)

        for s in range(n):
            for lhs, options in self.rules.items():
                for rhs in options:
                    if rhs == (target_symbols[s],):
                        v = R_index[lhs]
                        P[0, s, v] = True
        
        dual_productions = []
        for lhs, options in self.rules.items():
            for rhs in options:
                if len(rhs) == 2 and rhs[0] not in self.terminals and rhs[1] not in self.terminals:
                    # print(f"{lhs = }, {rhs[0] = }, {rhs[1] = }")
                    a = R_index[lhs]
                    b = R_index[rhs[0]]
                    c = R_index[rhs[1]]
                    dual_productions.append((a, b, c))
        pprint(self.rules)
        pprint(dual_productions)

        for l in range(1, n):
            print(f"running {l = }")
            for s in range(n - l + 1):
                for p in range(l):
                    print(f"  {l = }, {s = }, {p = }")
                    for a, b, c in dual_productions:
                        if P[p, s, b] and P[l - p, s + p, c]:
                            P[l, s, a] = True
                            back[(l, s, a)].append((p, b, c))
                # print(f"{l = }, {s = }, {P[l, s, :] = }")
        # print(P)
        print(np.any(P, axis=2))
        print(P[n - 1, 0, 0])
        # breakpoint()


def problem_1() -> None:
    substitutions: defaultdict[str, list[str]] = defaultdict(list)
    for line in lines:
        if "=>" in line:
            initial, replacement = line.split(" => ")
            substitutions[initial].append(replacement)
        elif line:
            molecule = line

    atoms = [
        "".join(atom_chars)
        for atom_chars in split_before(
            molecule,
            lambda s: s.isupper(),
        )
    ]

    one_step: set[str] = set()

    for idx, atom in enumerate(atoms):
        if atom in substitutions:
            for substitution in substitutions[atom]:
                one_step.add("".join(atoms[:idx]) + substitution + "".join(atoms[idx + 1 :]))

    print(len(one_step))


def problem_2() -> None:
    # grammar = CNFGrammar(
    #     [line.split(" => ") for line in lines[:-2]],
    #     lines[-1]
    # )
    # grammar.CYK()
    # grammar = CNFGrammar(
    #     [("e", "H"), ("e", "O"), ("H", "HO"), ("H", "OH"), ("O", "HH")],
    #     "HOHOHO",
    # )
    # grammar.CYK()
    grammar = CNFGrammar(
        [
            ("e", "NpVp"), ("Vp", "VpPp"), ("Vp", "VNp"), ("Vp", "Eats"), ("Pp", "PNp"), ("Np", "DetN"), ("Np", "She"), ("V", "Eats"), ("P", "With"), ("N", "Fish"), ("N", "Fork"), ("Det", "A")
        ],
        "SheEatsAFishWithAFork"
    )
    grammar.CYK()
