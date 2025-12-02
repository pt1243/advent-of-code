from __future__ import annotations

from copy import deepcopy
from itertools import product
from operator import attrgetter

with open("./2023/resources/22.txt") as f:
    lines = f.read().splitlines()


class Block:
    def __init__(self, start_x: int, start_y: int, start_z: int, end_x: int, end_y: int, end_z: int) -> None:
        self.positions = set(product(range(start_x, end_x + 1), range(start_y, end_y + 1), range(start_z, end_z + 1)))
        self.xy_positions = {pos[:2] for pos in self.positions}
        self.min_z = min(pos[2] for pos in self.positions)
        self.max_z = max(pos[2] for pos in self.positions)
        self.supported_by: list[Block] = []
        self.fell = False

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Block):
            return self.positions == other.positions
        return NotImplemented

    def is_underneath(self, other_block: Block) -> bool:
        return self.max_z == other_block.min_z - 1 and bool(self.xy_positions & other_block.xy_positions)


def problem_1() -> None:
    blocks: list[Block] = []
    for line in lines:
        left, right = line.split("~")
        start_x, start_y, start_z = (int(val) for val in left.split(","))
        end_x, end_y, end_z = (int(val) for val in right.split(","))
        blocks.append(Block(start_x, start_y, start_z, end_x, end_y, end_z))
    blocks.sort(key=attrgetter("min_z"))

    while True:
        any_moved = False
        for block in blocks:
            if block.min_z == 1:
                continue
            any_underneath = False
            for other_block in blocks:
                if other_block.is_underneath(block):
                    any_underneath = True
                    break
            if not any_underneath:
                block.positions = {(pos[0], pos[1], pos[2] - 1) for pos in block.positions}
                block.min_z -= 1
                block.max_z -= 1
                any_moved = True
        if not any_moved:
            break

    for block in blocks:
        for other_block in blocks:
            if block.is_underneath(other_block):
                other_block.supported_by.append(block)
    can_be_disintegrated = blocks.copy()
    for block in blocks:
        if len(block.supported_by) == 1 and block.supported_by[0] in can_be_disintegrated:
            can_be_disintegrated.remove(block.supported_by[0])
    print(len(can_be_disintegrated))


def problem_2() -> None:
    blocks: list[Block] = []
    for line in lines:
        left, right = line.split("~")
        start_x, start_y, start_z = (int(val) for val in left.split(","))
        end_x, end_y, end_z = (int(val) for val in right.split(","))
        blocks.append(Block(start_x, start_y, start_z, end_x, end_y, end_z))
    blocks.sort(key=attrgetter("min_z"))

    while True:
        any_moved = False
        for block in blocks:
            if block.min_z == 1:
                continue
            any_underneath = False
            for other_block in blocks:
                if other_block.is_underneath(block):
                    any_underneath = True
                    break
            if not any_underneath:
                block.positions = {(pos[0], pos[1], pos[2] - 1) for pos in block.positions}
                block.min_z -= 1
                block.max_z -= 1
                any_moved = True
        if not any_moved:
            break

    for block in blocks:
        for other_block in blocks:
            if block.is_underneath(other_block):
                other_block.supported_by.append(block)
    can_be_disintegrated = blocks.copy()
    for block in blocks:
        if len(block.supported_by) == 1 and block.supported_by[0] in can_be_disintegrated:
            can_be_disintegrated.remove(block.supported_by[0])

    total = 0
    for block_to_disintegrate in blocks:
        if block_to_disintegrate in can_be_disintegrated:
            continue
        new_blocks = deepcopy(blocks)
        supports_to_remove = [block_to_disintegrate]
        while supports_to_remove:
            support = supports_to_remove.pop()
            for block in new_blocks:
                if support in block.supported_by:
                    block.supported_by.remove(support)
                    if not block.supported_by:
                        block.fell = True
                        supports_to_remove.append(block)
        total += sum(1 for block in new_blocks if block.fell)
    print(total)
