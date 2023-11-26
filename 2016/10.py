from __future__ import annotations
from typing import ClassVar, Protocol


with open('./2016/resources/10.txt') as f:
    lines = [line.strip() for line in f]


class SupportsEvaluate(Protocol):
    def evaluate(self) -> int: ...


class Microchip:
    def __init__(self) -> None:
        pass


class InputBin:
    lookup: ClassVar[dict[int, InputBin]] = {}    

    def __init__(self, val: int) -> None:
        self.val = val
        InputBin.lookup[val] = self
    
    def evaluate(self) -> int:
        return self.val


class OutputBin:
    lookup: ClassVar[dict[int, OutputBin]] = {}

    def __init__(self, bin_num: int, value: int) -> None:
        self.bin_num = bin_num
        self.value = value
        OutputBin.lookup[bin_num] = self
    
    def evaluate(self) -> int:
        return self.value


class Bot:
    lookup: ClassVar[dict[int, Bot]] = {}

    def __init__(self, bot_num: int) -> None:
        self.bot_num = bot_num
        Bot.lookup[bot_num] = self
        self.values: list[SupportsEvaluate] = []
    
    # def add_
        


# def problem_1() -> None:
