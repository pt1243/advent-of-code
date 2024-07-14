from collections import defaultdict
import re

from more_itertools import split_before


with open("./2015/resources/19.txt") as f:
    lines = f.read().strip()


def problem_1() -> None:
    substitutions: defaultdict[str, list[str]] = defaultdict(list)
    all_rules, molecule = lines.split("\n\n")
    for rule in all_rules.split("\n"):
        initial, replacement = rule.split(" => ")
        substitutions[initial].append(replacement)

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
    all_rules, molecule = lines.split("\n\n")
    molecule = molecule[::-1]
    rules = {rule.split(" => ")[1][::-1]: rule.split(" => ")[0][::-1] for rule in all_rules.split("\n")}

    count = 0
    pattern = "|".join(rules.keys())

    def get_replacement(s: re.Match[str]) -> str:
        return rules[s.group()]

    while molecule != "e":
        molecule = re.sub(pattern, get_replacement, molecule, 1)
        count += 1

    print(count)
