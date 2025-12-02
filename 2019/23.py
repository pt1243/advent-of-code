from collections import defaultdict, deque
from itertools import batched

with open("./2019/resources/23.txt") as f:
    program = [int(num) for num in f.read().strip().split(",")]


class IntcodeProgram:
    def __init__(self, program: list[int], input_queue: list[int] | None = None) -> None:
        self.memory: defaultdict[int, int] = defaultdict(int)
        for i, val in enumerate(program):
            self.memory[i] = val
        self.i = 0
        self.relative_base = 0
        self.input_queue: deque[int] = deque(input_queue) if input_queue else deque()
        self.output_queue: deque[int] = deque()
        self.halted = False

    def _read_one_parameter(self) -> int:
        param_mode = self.memory[self.i] // 100
        if param_mode == 0:
            target_address = self.memory[self.i + 1]
            param = self.memory[target_address]
        elif param_mode == 1:
            param = self.memory[self.i + 1]
        elif param_mode == 2:
            target_address = self.memory[self.i + 1] + self.relative_base
            param = self.memory[target_address]
        else:
            raise ValueError(f"unknown mode for parameter {param_mode} with opcode {self.memory[self.i]}")
        return param

    def _get_write_address(self) -> int:
        param_mode = self.memory[self.i] // 100
        if param_mode == 0:
            write_address = self.memory[self.i + 1]
        elif param_mode == 2:
            write_address = self.memory[self.i + 1] + self.relative_base
        else:
            raise ValueError(f"unknown mode for parameter {param_mode} with opcode {self.memory[self.i]}")
        return write_address

    def _read_two_addresses(self) -> tuple[int, int]:
        second_param_mode, rest = divmod(self.memory[self.i], 1000)
        first_param_mode = rest // 100
        if first_param_mode == 0:
            target_address = self.memory[self.i + 1]
            first_param = self.memory[target_address]
        elif first_param_mode == 1:
            first_param = self.memory[self.i + 1]
        elif first_param_mode == 2:
            target_address = self.memory[self.i + 1] + self.relative_base
            first_param = self.memory[target_address]
        else:
            raise ValueError(f"unknown mode for parameter 1 {first_param_mode} with opcode {self.memory[self.i]}")
        if second_param_mode == 0:
            target_address = self.memory[self.i + 2]
            second_param = self.memory[target_address]
        elif second_param_mode == 1:
            second_param = self.memory[self.i + 2]
        elif second_param_mode == 2:
            target_address = self.memory[self.i + 2] + self.relative_base
            second_param = self.memory[target_address]
        else:
            raise ValueError(f"unknown mode for parameter 2 {second_param_mode} with opcode {self.memory[self.i]}")
        return first_param, second_param

    def _read_two_parameters_get_write_address(self) -> tuple[int, int, int]:
        third_param_mode, rest = divmod(self.memory[self.i], 10_000)
        second_param_mode, rest = divmod(rest, 1000)
        first_param_mode = rest // 100
        if first_param_mode == 0:
            write_address = self.memory[self.i + 1]
            first_param = self.memory[write_address]
        elif first_param_mode == 1:
            first_param = self.memory[self.i + 1]
        elif first_param_mode == 2:
            write_address = self.memory[self.i + 1] + self.relative_base
            first_param = self.memory[write_address]
        else:
            raise ValueError(f"unknown mode for parameter 1 {first_param_mode} with opcode {self.memory[self.i]}")
        if second_param_mode == 0:
            write_address = self.memory[self.i + 2]
            second_param = self.memory[write_address]
        elif second_param_mode == 1:
            second_param = self.memory[self.i + 2]
        elif second_param_mode == 2:
            write_address = self.memory[self.i + 2] + self.relative_base
            second_param = self.memory[write_address]
        else:
            raise ValueError(f"unknown mode for parameter 2 {second_param_mode} with opcode {self.memory[self.i]}")
        if third_param_mode == 0:
            write_address = self.memory[self.i + 3]
        elif third_param_mode == 2:
            write_address = self.memory[self.i + 3] + self.relative_base
        else:
            raise ValueError(f"unknown mode for parameter 3 {third_param_mode} with opcode {self.memory[self.i]}")
        return first_param, second_param, write_address

    def _add(self) -> None:
        first_param, second_param, write_address = self._read_two_parameters_get_write_address()
        self.memory[write_address] = first_param + second_param
        self.i += 4

    def _multiply(self) -> None:
        first_param, second_param, write_address = self._read_two_parameters_get_write_address()
        self.memory[write_address] = first_param * second_param
        self.i += 4

    def _input(self) -> bool:
        write_address = self._get_write_address()
        if not self.input_queue:
            return False
        self.memory[write_address] = self.input_queue.popleft()
        self.i += 2
        return True

    def _output(self) -> None:
        param = self._read_one_parameter()
        self.output_queue.append(param)
        self.i += 2

    def _jump_if_true(self) -> None:
        first_param, second_param = self._read_two_addresses()
        if first_param != 0:
            self.i = second_param
        else:
            self.i += 3

    def _jump_if_false(self) -> None:
        first_param, second_param = self._read_two_addresses()
        if first_param == 0:
            self.i = second_param
        else:
            self.i += 3

    def _less_than(self) -> None:
        first_param, second_param, write_address = self._read_two_parameters_get_write_address()
        self.memory[write_address] = 1 if first_param < second_param else 0
        self.i += 4

    def _equals(self) -> None:
        first_param, second_param, write_address = self._read_two_parameters_get_write_address()
        self.memory[write_address] = 1 if first_param == second_param else 0
        self.i += 4

    def _relative_base_offset(self) -> None:
        param = self._read_one_parameter()
        self.relative_base += param
        self.i += 2

    def run(self) -> None:
        if self.halted:
            raise ValueError("program has already halted")
        while True:
            opcode = self.memory[self.i] % 100
            if opcode == 1:
                self._add()
            elif opcode == 2:
                self._multiply()
            elif opcode == 3:
                has_input = self._input()
                if not has_input:
                    return
            elif opcode == 4:
                self._output()
            elif opcode == 5:
                self._jump_if_true()
            elif opcode == 6:
                self._jump_if_false()
            elif opcode == 7:
                self._less_than()
            elif opcode == 8:
                self._equals()
            elif opcode == 9:
                self._relative_base_offset()
            elif opcode == 99:
                self.halted = True
                return
            else:
                raise ValueError(f"unknown opcode {opcode} at index {self.i}")


def problem_1() -> None:
    computers = {i: IntcodeProgram(program, [i]) for i in range(50)}
    while True:
        for computer in computers.values():
            if not computer.input_queue:
                computer.input_queue.append(-1)
            computer.run()
            for dest, x, y in batched(computer.output_queue, 3):
                if dest == 255:
                    print(y)
                    return
                computers[dest].input_queue.extend((x, y))
            computer.output_queue.clear()


def problem_2() -> None:
    computers = {i: IntcodeProgram(program, [i]) for i in range(50)}
    nat_packet = (0, 0)
    last_nat_packet_sent = (0, 0)
    while True:
        all_idle = True
        for computer in computers.values():
            if computer.input_queue:
                all_idle = False
            else:
                computer.input_queue.append(-1)
            computer.run()
            if computer.output_queue:
                all_idle = False
            for dest, x, y in batched(computer.output_queue, 3):
                if dest == 255:
                    nat_packet = (x, y)
                else:
                    computers[dest].input_queue.extend((x, y))
            computer.output_queue.clear()
        if all_idle:
            if nat_packet[1] == last_nat_packet_sent[1]:
                print(nat_packet[1])
                return
            computers[0].input_queue.extend(nat_packet)
            last_nat_packet_sent = nat_packet
