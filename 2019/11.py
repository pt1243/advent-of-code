from collections import defaultdict, deque

with open("./2019/resources/11.txt") as f:
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


def part_1() -> None:
    panels: defaultdict[tuple[int, int], int] = defaultdict(int)
    panels_painted: set[tuple[int, int]] = set()
    row, col = 0, 0
    direction = 0
    directions = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
    robot = IntcodeProgram(program)
    while not robot.halted:
        robot.input_queue.append(panels[row, col])
        robot.run()
        colour = robot.output_queue.popleft()
        turn = robot.output_queue.popleft()
        panels[row, col] = colour
        panels_painted.add((row, col))
        direction += 1 if turn else -1
        direction %= 4
        drow, dcol = directions[direction]
        row += drow
        col += dcol
    print(len(panels_painted))


def part_2() -> None:
    panels: defaultdict[tuple[int, int], int] = defaultdict(int)
    panels[0, 0] = 1
    panels_painted: set[tuple[int, int]] = set()
    row, col = 0, 0
    direction = 0
    directions = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
    robot = IntcodeProgram(program)
    while not robot.halted:
        robot.input_queue.append(panels[row, col])
        robot.run()
        colour = robot.output_queue.popleft()
        turn = robot.output_queue.popleft()
        panels[row, col] = colour
        panels_painted.add((row, col))
        direction += 1 if turn else -1
        direction %= 4
        drow, dcol = directions[direction]
        row += drow
        col += dcol
    min_row = min(pos[0] for pos in panels)
    max_row = max(pos[0] for pos in panels)
    min_col = min(pos[1] for pos in panels)
    max_col = max(pos[1] for pos in panels)
    for row in range(min_row, max_row + 1):
        row_string = ""
        for col in range(min_col, max_col + 1):
            row_string += "█" if panels[row, col] else " "
        print(row_string)
