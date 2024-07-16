from __future__ import annotations
from typing import ClassVar, Protocol, Literal


with open("./2016/resources/10.txt") as f:
    lines = [line.strip() for line in f]


class Bot:
    lookup: ClassVar[dict[int, Bot]] = {}
    outputs: ClassVar[dict[int, int]] = {}

    def __init__(
        self,
        bot_num: int,
        low_type: Literal["bot", "output"],
        low_target: int,
        high_type: Literal["bot", "output"],
        high_target: int,
    ) -> None:
        self.bot_num = bot_num
        Bot.lookup[bot_num] = self
        self.values: list[int] = []
        self.low_type = low_type
        self.low_target = low_target
        self.high_type = high_type
        self.high_target = high_target

    def add_microchip(self, value: int, add_to_output: bool = False) -> None:
        self.values.append(value)
        if len(self.values) == 2:
            a, b = self.values
            low = a if a <= b else b
            high = b if low == a else a

            if low == 17 and high == 61 and not add_to_output:
                print(self.bot_num)
                return

            if self.low_type == "bot":
                Bot.lookup[self.low_target].add_microchip(low, add_to_output=add_to_output)
            elif add_to_output:
                Bot.outputs[self.low_target] = low
            if self.high_type == "bot":
                Bot.lookup[self.high_target].add_microchip(high, add_to_output=add_to_output)
            elif add_to_output:
                Bot.outputs[self.high_target] = high


def problem_1() -> None:
    # create all bots first
    for line in lines:
        if line.startswith("bot"):
            split = line.split()
            bot_num = int(split[1])
            low_type = split[5]
            low_target = int(split[6])
            high_type = split[10]
            high_target = int(split[11])
            Bot(bot_num, low_type, low_target, high_type, high_target)  # type: ignore[arg-type]

    for line in lines:
        if line.startswith("value"):
            split = line.split()
            target_bot = int(split[5])
            val = int(split[1])
            Bot.lookup[target_bot].add_microchip(val)


def problem_2() -> None:
    # create all bots first
    for line in lines:
        if line.startswith("bot"):
            split = line.split()
            bot_num = int(split[1])
            low_type = split[5]
            low_target = int(split[6])
            high_type = split[10]
            high_target = int(split[11])
            Bot(bot_num, low_type, low_target, high_type, high_target)  # type: ignore[arg-type]

    for line in lines:
        if line.startswith("value"):
            split = line.split()
            target_bot = int(split[5])
            val = int(split[1])
            Bot.lookup[target_bot].add_microchip(val, add_to_output=True)

    print(Bot.outputs[0] * Bot.outputs[1] * Bot.outputs[2])
