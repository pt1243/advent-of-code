from collections import defaultdict
from collections.abc import Iterable
import heapq
import re
from string import ascii_lowercase, ascii_uppercase
from typing import NamedTuple
from time import sleep

from more_itertools import split_when


with open('./2015/resources/19.txt') as f:
    lines = [line.strip() for line in f]


def split_into_atoms(s: str) -> list[str]:
    return list("".join(atom_chars) for atom_chars in split_when(s, lambda c1, c2: (c1 in ascii_lowercase and c2 in ascii_uppercase) or (c1 in ascii_uppercase and c2 in ascii_uppercase)))


class StringCandidate(NamedTuple):
    weight: int
    steps: int
    content: str


def find_substring(s: str, sub: str) -> Iterable[int]:  # note: should inline for better performance
    min_index = 0
    while True:
        found_idx = s.find(sub, min_index)
        if found_idx == -1:
            break
        yield found_idx
        min_index = found_idx + 1


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
    unsorted: dict[str, str] = {}
    for line in lines:
        if "=>" in line:
            replacement, initial = line.split(" => ")
            # print(f"{initial = }, {replacement = }")
            unsorted[initial] = replacement
        elif line:
            final_molecule = line
    
    substitutions = {initial: unsorted[initial] for initial in sorted(unsorted.keys(), key=len, reverse=True)}
    
    # def solve(s: str) -> int:
    #     print(f"called with {s = }")
    #     if s == "e":
    #         return 0
    #     solution = (solve(s.replace(initial, replacement)) for initial, replacement in substitutions.items() if initial in s)
    #     return next(solution) + 1
    
    # print(solve(final_molecule))

    from pprint import pprint
    print(substitutions)

    current = final_molecule
    steps = 0
    while current != "e":
        for initial, replacement in unsorted.items():
            if initial in current:
                current = current.replace(initial, replacement)
                steps += 1
                break
        print(f"{current = }")
    print(steps)


    # final_molecule_length = len(final_molecule)
    # stack = ["e"]
    # steps: dict[str, int] = {"e": 0}
    # seen: set[str] = set()
    # seen_seen: set[int] = set()

    # while stack:
    #     current = stack.pop()
    #     # seen.add(current)
    #     current_steps = steps[current]
    #     length_1000 = len(seen) // 1000
    #     if length_1000 not in seen_seen:
    #         print(f"current stack length = {len(stack)}, {current_steps = }, number seen = {len(seen)}")
    #         seen_seen.add(length_1000)
    #     for initial, replacements in substitutions.items():
    #         if initial in current:
    #             # print(f"checking {initial = }, {replacements = }")
    #             len_initial = len(initial)
    #             min_index = 0
    #             while True:
    #                 start_idx = current.find(initial, min_index)
    #                 if start_idx == -1:
    #                     break
    #             # for start_idx in find_substring(current, initial):
    #                 # print(f"checking {start_idx = }")
    #                 for replacement in replacements:
    #                     new = current[:start_idx] + replacement + current[start_idx+len_initial:]
    #                     if len(new) > final_molecule_length or new in seen:
    #                         continue
    #                     new_steps = current_steps + 1
    #                     steps[new] = new_steps
    #                     # if new_steps > 1
    #                     if new == final_molecule:
    #                         print(new)
    #                         print(new_steps)
    #                         return
    #                     stack.append(new)
    #                     seen.add(new)
    #                 min_index = start_idx + 1


                

    # len_final_molecule = len(final_molecule)
    # # print(substitutions)
    # found: set[str] = set()
    # queue: list[StringCandidate] = [StringCandidate(len_final_molecule - len("e"), 0, "e")]

    # # need to use bisect
    
    # def search():
    #     while True:
    #         current_item = heapq.heappop(queue)
    #         current = current_item.content
    #         current_steps = current_item.steps
    #         # print(f"current weight = {current_item.weight}, queue length = {len(queue)}, found length = {len(found)}")
    #         steps = current_steps + 1
    #         if steps > 10_000:  # guess
    #             continue
    #         for initial, replacements in substitutions.items():
    #             if initial in current:
    #                 min_index = 0
    #                 len_initial = len(initial)
    #                 while True:
    #                     index_found = current.find(initial, min_index)
    #                     if index_found == -1:
    #                         break
    #                     prev, post = current[:index_found], current[index_found+len_initial:]
    #                     for replacement in replacements:
    #                         new = prev + replacement + post
    #                         if len(new) > len_final_molecule:
    #                             continue
    #                         if new == final_molecule:
    #                             print(steps)
    #                             return
    #                         weight = abs(len_final_molecule - len(new))
                            
    #                         if new not in found:
    #                             found.add(new)
    #                             item = StringCandidate(weight, steps, new)
    #                             heapq.heappush(queue, item)
                            
    #                     min_index = index_found + 1

    # search()
