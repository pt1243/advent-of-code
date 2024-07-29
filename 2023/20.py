from __future__ import annotations
from collections import deque
from itertools import count
from math import lcm
from typing import ClassVar, Literal


with open("./2023/resources/20.txt") as f:
    lines = [line.strip() for line in f]


class Module:
    lookup: ClassVar[dict[str, Module]] = {}
    num_low_pulses = 0
    num_high_pulses = 0
    pulse_queue: ClassVar[deque[tuple[str, Module, bool]]] = deque()
    rx_aggregator_inputs: ClassVar[dict[str, int | None]] = {}

    def __init__(
        self, module_type: Literal["broadcaster", "flip-flop", "conjunction", "rx"], name: str, destinations: list[str]
    ) -> None:
        type(self).lookup[name] = self
        self.name = name
        self.module_type = module_type
        self.destination_strings = destinations
        self.destinations: list[Module] = []
        self.inputs: dict[str, bool] = {}
        self.flip_flop_state = False

    @classmethod
    def update_destinations(cls) -> None:
        for module in cls.lookup.values():
            for dest_string in module.destination_strings:
                module.destinations.append(cls.lookup[dest_string])

    @classmethod
    def construct_conjunction_inputs(cls) -> None:
        for module_str, module in cls.lookup.items():
            for dest in module.destinations:
                if dest.module_type == "conjunction":
                    dest.inputs[module_str] = False

    def process_input(self, sender: str, pulse_type: bool) -> None:
        # print(f"{sender} -{'high' if pulse_type else 'low'}-> {self.name}")
        if self.module_type == "flip-flop":
            if not pulse_type:
                self.flip_flop_state = not self.flip_flop_state
                self.send(self.flip_flop_state)
        elif self.module_type == "conjunction":
            self.inputs[sender] = pulse_type
            self.send(not all(self.inputs.values()))
        elif self.module_type == "broadcaster":
            self.send(pulse_type)

    def send(self, pulse_type: bool) -> None:
        for dest in self.destinations:
            type(self).pulse_queue.append((self.name, dest, pulse_type))
        if pulse_type:
            type(self).num_high_pulses += len(self.destinations)
        else:
            type(self).num_low_pulses += len(self.destinations)

    @classmethod
    def push_button(cls, num: int = 0, watch_for_high: list[Module] | None = None) -> bool:
        broadcaster = cls.lookup["broadcaster"]
        broadcaster.process_input("button", False)
        cls.num_low_pulses += 1
        while cls.pulse_queue:
            source, dest, pulse_type = cls.pulse_queue.popleft()
            if watch_for_high:
                if dest in watch_for_high and not pulse_type:
                    cls.rx_aggregator_inputs[source] = num
            dest.process_input(source, pulse_type)

    @classmethod
    def get_times_to_button_inputs(cls) -> dict[str, int]:
        rx = cls.lookup["rx"]
        rx_aggregator = [m for m in cls.lookup.values() if rx in m.destinations][0]
        inputs_to_aggregator = [m for m in cls.lookup.values() if rx_aggregator in m.destinations]
        inputs_to_inputs = [m for m in cls.lookup.values() if any(d in m.destinations for d in inputs_to_aggregator)]
        for module_to_watch in inputs_to_inputs:
            cls.rx_aggregator_inputs[module_to_watch.name] = None
        for num in count(1):
            cls.push_button(num, inputs_to_aggregator)
            if all(time_to_high is not None for time_to_high in cls.rx_aggregator_inputs.values()):
                return cls.rx_aggregator_inputs


def problem_1() -> None:
    for line in lines:
        name_and_type, destinations = line.split(" -> ")
        if name_and_type == "broadcaster":
            module_type, name = "broadcaster", "broadcaster"
        else:
            type_str = name_and_type[0]
            module_type = "flip-flop" if type_str == "%" else "conjunction"
            name = name_and_type[1:]
        Module(module_type, name, destinations.split(", "))
    Module("rx", "rx", [])

    Module.update_destinations()
    Module.construct_conjunction_inputs()
    for _ in range(1000):
        Module.push_button()
    print(Module.num_low_pulses * Module.num_high_pulses)


def problem_2() -> None:
    for line in lines:
        name_and_type, destinations = line.split(" -> ")
        if name_and_type == "broadcaster":
            module_type, name = "broadcaster", "broadcaster"
        else:
            type_str = name_and_type[0]
            module_type = "flip-flop" if type_str == "%" else "conjunction"
            name = name_and_type[1:]
        Module(module_type, name, destinations.split(", "))
    Module("rx", "rx", [])

    Module.update_destinations()
    Module.construct_conjunction_inputs()

    lcm_times = Module.get_times_to_button_inputs()
    print(lcm(*lcm_times.values()))
