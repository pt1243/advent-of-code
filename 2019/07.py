from collections import deque
from itertools import permutations

with open("./2019/resources/7.txt") as f:
    program = [int(num) for num in f.read().strip().split(",")]


class IntcodeProgram:
    def __init__(self, program: list[int], input_queue: list[int] | None = None) -> None:
        self.memory = program
        self.i = 0
        self.input_queue: deque[int] = deque(input_queue) if input_queue else deque()
        self.output_queue: deque[int] = deque()
        self.halted = False

    def _get_one_parameter(self) -> int:
        param_mode = self.memory[self.i] // 100
        if param_mode == 0:
            target_address = self.memory[self.i + 1]
            param = self.memory[target_address]
        elif param_mode == 1:
            param = self.memory[self.i + 1]
        else:
            raise ValueError(f"unknown mode for parameter {param_mode} with opcode {self.memory[self.i]}")
        return param

    def _get_two_parameters(self) -> tuple[int, int]:
        second_param_mode, rest = divmod(self.memory[self.i], 1000)
        first_param_mode = rest // 100
        if first_param_mode == 0:
            target_address = self.memory[self.i + 1]
            first_param = self.memory[target_address]
        elif first_param_mode == 1:
            first_param = self.memory[self.i + 1]
        else:
            raise ValueError(f"unknown mode for parameter 1 {first_param_mode} with opcode {self.memory[self.i]}")
        if second_param_mode == 0:
            target_address = self.memory[self.i + 2]
            second_param = self.memory[target_address]
        elif second_param_mode == 1:
            second_param = self.memory[self.i + 2]
        else:
            raise ValueError(f"unknown mode for parameter 2 {second_param_mode} with opcode {self.memory[self.i]}")
        return first_param, second_param

    def _add(self) -> None:
        first_param, second_param = self._get_two_parameters()
        target_address = self.memory[self.i + 3]
        self.memory[target_address] = first_param + second_param
        self.i += 4

    def _multiply(self) -> None:
        first_param, second_param = self._get_two_parameters()
        target_address = self.memory[self.i + 3]
        self.memory[target_address] = first_param * second_param
        self.i += 4

    def _input(self) -> bool:
        target_address = self.memory[self.i + 1]
        if not self.input_queue:
            return False
        self.memory[target_address] = self.input_queue.popleft()
        self.i += 2
        return True

    def _output(self) -> None:
        param = self._get_one_parameter()
        self.output_queue.append(param)
        self.i += 2

    def _jump_if_true(self) -> None:
        first_param, second_param = self._get_two_parameters()
        if first_param != 0:
            self.i = second_param
        else:
            self.i += 3

    def _jump_if_false(self) -> None:
        first_param, second_param = self._get_two_parameters()
        if first_param == 0:
            self.i = second_param
        else:
            self.i += 3

    def _less_than(self) -> None:
        first_param, second_param = self._get_two_parameters()
        target_index = self.memory[self.i + 3]
        self.memory[target_index] = 1 if first_param < second_param else 0
        self.i += 4

    def _equals(self) -> None:
        first_param, second_param = self._get_two_parameters()
        target_index = self.memory[self.i + 3]
        self.memory[target_index] = 1 if first_param == second_param else 0
        self.i += 4

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
            elif opcode == 99:
                self.halted = True
                return
            else:
                raise ValueError(f"unknown opcode {opcode} at index {self.i}")


def part_1() -> None:
    max_thruster_signal = 0
    for phase_settings in permutations(range(5), 5):
        amp_a = IntcodeProgram(program, [phase_settings[0], 0])
        amp_a.run()
        amp_b = IntcodeProgram(program, [phase_settings[1], amp_a.output_queue.popleft()])
        amp_b.run()
        amp_c = IntcodeProgram(program, [phase_settings[2], amp_b.output_queue.popleft()])
        amp_c.run()
        amp_d = IntcodeProgram(program, [phase_settings[3], amp_c.output_queue.popleft()])
        amp_d.run()
        amp_e = IntcodeProgram(program, [phase_settings[4], amp_d.output_queue.popleft()])
        amp_e.run()
        thruster_signal = amp_e.output_queue.popleft()
        max_thruster_signal = max(max_thruster_signal, thruster_signal)
    print(max_thruster_signal)


def part_2() -> None:
    max_thruster_signal = 0
    for phase_settings in permutations(range(5, 10), 5):
        amp_a = IntcodeProgram(program, [phase_settings[0]])
        amp_b = IntcodeProgram(program, [phase_settings[1]])
        amp_c = IntcodeProgram(program, [phase_settings[2]])
        amp_d = IntcodeProgram(program, [phase_settings[3]])
        amp_e = IntcodeProgram(program, [phase_settings[4]])
        start_of_loop_val = 0
        while not amp_e.halted:
            amp_a.input_queue.append(start_of_loop_val)
            amp_a.run()
            amp_b.input_queue.append(amp_a.output_queue.popleft())
            amp_b.run()
            amp_c.input_queue.append(amp_b.output_queue.popleft())
            amp_c.run()
            amp_d.input_queue.append(amp_c.output_queue.popleft())
            amp_d.run()
            amp_e.input_queue.append(amp_d.output_queue.popleft())
            amp_e.run()
            start_of_loop_val = amp_e.output_queue.popleft()
        thruster_signal = start_of_loop_val
        max_thruster_signal = max(max_thruster_signal, thruster_signal)
    print(max_thruster_signal)
