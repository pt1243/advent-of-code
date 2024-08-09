from collections import defaultdict, deque
import heapq
from itertools import count, pairwise


with open("./2019/resources/15.txt") as f:
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


def a_star(open_space: set[tuple[int, int]], start: tuple[int, int], end: tuple[int, int]) -> list[tuple[int, int]]:
    offsets = ((-1, 0), (0, 1), (0, -1), (1, 0))
    open_set = [(0, start)]
    came_from: dict[tuple[int, int], tuple[int, int]] = {}
    g_score: defaultdict[tuple[int, int], int] = defaultdict(lambda: 10**12)
    g_score[start] = 0
    f_score: defaultdict[tuple[int, int], int] = defaultdict(lambda: 10**12)
    f_score[start] = abs(start[0] - end[0]) + abs(start[1] - end[1])
    while open_set:
        _, current = heapq.heappop(open_set)
        if current == end:
            total_path = [current]
            while current in came_from:
                current = came_from[current]
                total_path.append(current)
            return total_path[::-1]
        row, col = current
        current_g_score = g_score[current]
        for drow, dcol in offsets:
            neighbour = (row + drow, col + dcol)
            if neighbour in open_space:
                tentative_g_score = current_g_score + 1
                if tentative_g_score < g_score[neighbour]:
                    came_from[neighbour] = current
                    g_score[neighbour] = tentative_g_score
                    f_score[neighbour] = tentative_g_score + abs(neighbour[0] - end[0]) + abs(neighbour[1] - end[1])
                    heapq.heappush(open_set, (f_score[neighbour], neighbour))
    raise ValueError("could not find path")


def explore_map() -> tuple[tuple[int, int], set[tuple[int, int]]]:
    offsets = ((-1, 0), (1, 0), (0, -1), (0, 1))
    reverse_movements = {1: 2, 2: 1, 3: 4, 4: 3}
    open_space: set[tuple[int, int]] = {(0, 0)}
    walls: set[tuple[int, int]] = set()
    current_position = (0, 0)
    oxygen_system_location = (0, 0)
    repair_droid = IntcodeProgram(program)

    spaces_to_explore = [current_position]
    while spaces_to_explore:
        target = spaces_to_explore.pop()
        path = a_star(open_space, current_position, target)
        movement_commands = [offsets.index((p2[0] - p1[0], p2[1] - p1[1])) + 1 for p1, p2 in pairwise(path)]
        repair_droid.input_queue.extend(movement_commands)
        repair_droid.run()
        repair_droid.output_queue.clear()
        current_position = target
        for command, offset in enumerate(offsets, start=1):
            new_position = (current_position[0] + offset[0], current_position[1] + offset[1])
            if new_position in open_space or new_position in walls:
                continue
            repair_droid.input_queue.append(command)
            repair_droid.run()
            movement_status = repair_droid.output_queue.popleft()
            if movement_status == 0:
                walls.add(new_position)
            else:
                if movement_status == 2:
                    oxygen_system_location = new_position
                open_space.add(new_position)
                spaces_to_explore.append(new_position)
                repair_droid.input_queue.append(reverse_movements[command])
                repair_droid.run()
                repair_droid.output_queue.popleft()
    return oxygen_system_location, open_space


def problem_1() -> None:
    oxygen_system_location, open_space = explore_map()
    path_to_oxygen_system = a_star(open_space, (0, 0), oxygen_system_location)
    print(len(path_to_oxygen_system) - 1)


def problem_2() -> None:
    oxygen_system_location, open_space = explore_map()

    has_oxygen = {oxygen_system_location}
    frontier = {oxygen_system_location}
    offsets = ((-1, 0), (1, 0), (0, -1), (0, 1))

    for i in count(1):
        new_frontier = set()
        for position in frontier:
            for offset in offsets:
                new_position = (position[0] + offset[0], position[1] + offset[1])
                if new_position in open_space and new_position not in has_oxygen:
                    new_frontier.add(new_position)
        has_oxygen.update(new_frontier)
        if not open_space - has_oxygen:
            print(i)
            return
        frontier = new_frontier
