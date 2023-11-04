from collections import defaultdict
from collections.abc import Iterable
from string import ascii_lowercase, ascii_uppercase

from more_itertools import split_when


with open('./2015/resources/19.txt') as f:
    lines = [line.strip() for line in f]


def split_into_atoms(s: str) -> list[str]:
    return list("".join(atom_chars) for atom_chars in split_when(s, lambda c1, c2: (c1 in ascii_lowercase and c2 in ascii_uppercase) or (c1 in ascii_uppercase and c2 in ascii_uppercase)))


class Queue:
    def __init__(self, items: Iterable[str] | None = None) -> None:
        self.items: set[str] = set(items) if items else set()

    def get(self) -> str:
        item = min(self.items)
        self.items.remove(item)
        return item

    def add(self, item: str) -> None:
        self.items.add(item)


def problem_1():
    substitutions: defaultdict[str, list[str]] = defaultdict(list)
    for line in lines:
        if "=>" in line:
            initial, replacement = line.split(" => ")
            substitutions[initial].append(replacement)
        elif line:
            molecule = line
    
    atoms = split_into_atoms(molecule)
    
    one_step: set[str] = set()

    for idx, atom in enumerate(atoms):
        if atom in substitutions:
            for substitution in substitutions[atom]:
                one_step.add("".join(atoms[:idx]) + substitution + "".join(atoms[idx+1:]))
    
    print(len(one_step))


def problem_2():
    substitutions: defaultdict[str, list[str]] = defaultdict(list)
    for line in lines:
        if "=>" in line:
            replacement, initial = line.split(" => ")
            substitutions[initial].append(replacement)
        elif line:
            final_molecule = line

    steps = 0
    queue = Queue((final_molecule,))
    found: set[str] = set()
    