from collections import defaultdict, deque
from itertools import batched

from more_itertools import sliding_window, split_when


with open("./2019/resources/17.txt") as f:
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


def get_scaffold() -> tuple[str, list[str]]:
    vacuum_robot = IntcodeProgram(program)
    vacuum_robot.run()
    ascii_output = "".join(chr(x) for x in vacuum_robot.output_queue)[:-1]
    scaffold = ascii_output.splitlines()
    return ascii_output, scaffold


def problem_1() -> None:
    _, scaffold = get_scaffold()
    sum_of_alignment_parameters = 0
    for i, line in enumerate(scaffold[1:-1], start=1):
        for j, char in enumerate(line[1:-1], start=1):
            if (
                char == "#"
                and scaffold[i - 1][j] == "#"
                and scaffold[i + 1][j] == "#"
                and scaffold[i][j - 1] == "#"
                and scaffold[i][j + 1] == "#"
            ):
                sum_of_alignment_parameters += i * j
    print(sum_of_alignment_parameters)


def problem_2() -> None:
    ascii_output, scaffold = get_scaffold()

    def get_path(ascii_output: str, scaffold: list[str]) -> list[tuple[str, ...]]:
        robot_directions = "^>v<"
        robot_char = ""
        for char in robot_directions:
            if char in ascii_output:
                robot_char = char
                break

        starting_row, starting_col = 0, 0
        for starting_row, line in enumerate(scaffold):
            if robot_char in line:
                starting_col = line.index(robot_char)
                break

        width, height = len(scaffold[0]), len(scaffold)
        offsets = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
        current_position = (starting_row, starting_col)
        path: list[str] = []
        direction = robot_directions.index(robot_char)

        current_steps = 0
        while True:
            # try to step forward
            offset = offsets[direction]
            next_position = (current_position[0] + offset[0], current_position[1] + offset[1])
            if (
                0 <= next_position[0] < height
                and 0 <= next_position[1] < width
                and scaffold[next_position[0]][next_position[1]] == "#"
            ):
                current_steps += 1
                current_position = next_position
                continue
            else:  # turn
                turn_offset = offsets[(direction - 1) % 4]
                turn_position = (current_position[0] + turn_offset[0], current_position[1] + turn_offset[1])
                if (
                    0 <= turn_position[0] < height
                    and 0 <= turn_position[1] < width
                    and scaffold[turn_position[0]][turn_position[1]] == "#"
                ):
                    direction -= 1
                    direction %= 4
                    if current_steps:
                        path.append(str(current_steps))
                    path.append("L")
                    current_steps = 0
                    continue
                turn_offset = offsets[(direction + 1) % 4]
                turn_position = (current_position[0] + turn_offset[0], current_position[1] + turn_offset[1])
                if (
                    0 <= turn_position[0] < height
                    and 0 <= turn_position[1] < width
                    and scaffold[turn_position[0]][turn_position[1]] == "#"
                ):
                    direction += 1
                    direction %= 4
                    if current_steps:
                        path.append(str(current_steps))
                    path.append("R")
                    current_steps = 0
                    continue
                path.append(str(current_steps))
                return list(batched(path, 2))

    def get_routine_and_subroutines(path_pairs: list[tuple[str, ...]]) -> tuple[str, str, str, str]:
        all_As = [[path_pairs[0]]]
        while (
            len([window for window in sliding_window(path_pairs, len(all_As[-1])) if window == tuple(all_As[-1])]) > 1
            and len(",".join(item[0] + "," + item[1] for item in all_As[-1])) <= 20
        ):
            all_As.append(path_pairs[: len(all_As[-1]) + 1])
        all_As.pop()
        A = all_As.pop()

        while True:
            # we now need to mark the items used by A, so they cannot be reused by C
            used_by_A = [False for _ in path_pairs]
            for i in [i for i, window in enumerate(sliding_window(path_pairs, len(A))) if window == tuple(A)]:
                used_by_A[i : i + len(A)] = [True] * len(A)

            # make C (the end) as long as possible
            all_Cs = [[path_pairs[-1]]]
            while (
                len(
                    [
                        window
                        for i, window in enumerate(sliding_window(path_pairs, len(all_Cs[-1])))
                        if window == tuple(all_Cs[-1]) and not any(used_by_A[i : i + len(all_Cs[-1])])
                    ]
                )
                > 1
                and len(",".join(item[0] + "," + item[1] for item in all_Cs[-1])) <= 20
            ):
                all_Cs.append(path_pairs[-len(all_Cs[-1]) - 1 :])
            all_Cs.pop()
            C = all_Cs.pop()

            while True:
                # mark the spaces used by C
                used_by_C = [False for _ in path_pairs]
                for i in [
                    i
                    for i, window in enumerate(sliding_window(path_pairs, len(C)))
                    if window == tuple(C) and not any(used_by_A[i : i + len(C)])
                ]:
                    used_by_C[i : i + len(C)] = [True] * len(C)

                # get the spaces used by B
                used_by_B = [
                    not (is_used_by_A or is_used_by_C) for is_used_by_A, is_used_by_C in zip(used_by_A, used_by_C)
                ]

                indices_used_by_b = [i for i, val in enumerate(used_by_B) if val]
                groups = list(split_when(indices_used_by_b, lambda x1, x2: abs(x1 - x2) > 1))
                lengths = [len(g) for g in groups]
                possible_b_lengths = [
                    i for i in range(1, max(lengths) + 1) if all(length % i == 0 for length in lengths)
                ]
                for b_length in possible_b_lengths:
                    first_occurrence_index = indices_used_by_b[:b_length]
                    first_occurrence = path_pairs[first_occurrence_index[0] : first_occurrence_index[-1] + 1]
                    for index_group in batched(indices_used_by_b, b_length):
                        occcurence = path_pairs[index_group[0] : index_group[-1] + 1]
                        if occcurence != first_occurrence:
                            break
                    else:
                        B = first_occurrence
                        # now, we need to break the full sequence into the A, B, and C actually used
                        i = 0
                        subroutines = []
                        while i < len(path_pairs):
                            if used_by_A[i]:
                                subroutines.append("A")
                                i += len(A)
                            elif used_by_B[i]:
                                subroutines.append("B")
                                i += len(B)
                            elif used_by_C[i]:
                                subroutines.append("C")
                                i += len(C)
                        main_routine_text = ",".join(subroutines) + "\n"
                        A_text = ",".join(item[0] + "," + item[1] for item in A) + "\n"
                        B_text = ",".join(item[0] + "," + item[1] for item in B) + "\n"
                        C_text = ",".join(item[0] + "," + item[1] for item in C) + "\n"
                        return main_routine_text, A_text, B_text, C_text

                # otherwise, if nothing works, try backing off from C and recomputing B
                if all_Cs:
                    C = all_Cs.pop()
                else:
                    break
            # if we have run out of Cs to try, try backing off from A, and starting with C all over again
            A = all_As.pop()

    path_pairs = get_path(ascii_output, scaffold)
    main_routine_text, A_text, B_text, C_text = get_routine_and_subroutines(path_pairs)

    program[0] = 2
    vacuum_robot = IntcodeProgram(program)
    vacuum_robot.input_queue.extend([ord(c) for c in main_routine_text])
    vacuum_robot.input_queue.extend([ord(c) for c in A_text])
    vacuum_robot.input_queue.extend([ord(c) for c in B_text])
    vacuum_robot.input_queue.extend([ord(c) for c in C_text])
    vacuum_robot.input_queue.append(ord("n"))
    vacuum_robot.input_queue.append(ord("\n"))
    vacuum_robot.run()

    print(vacuum_robot.output_queue.pop())
