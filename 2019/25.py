from collections import defaultdict, deque
from more_itertools import powerset_of_sets


with open("./2019/resources/25.txt") as f:
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
    opposite_directions = {"north": "south", "south": "north", "east": "west", "west": "east"}
    unsafe_items = {"escape pod", "giant electromagnet", "infinite loop", "molten lava", "photons"}
    items: list[str] = []

    droid = IntcodeProgram(program)
    droid.run()
    output_text = "".join(chr(x) for x in droid.output_queue).strip("\n")
    blocks = output_text.split("\n\n")
    room_info = blocks[0]
    current_room = room_info[room_info.index("==") + 3 : room_info.rindex("==") - 1]
    connections: defaultdict[str, dict[str, str]] = defaultdict(dict)
    doors = blocks[1]
    for door in doors.split("\n")[1:]:
        connections[current_room][door[2:]] = ""

    def path_from(source: str, dest: str) -> tuple[str, ...]:
        queue: deque[tuple[tuple[str, ...], tuple[str, ...]]] = deque([((source,), ())])
        while queue:
            all_rooms, movements = queue.popleft()
            current_room = all_rooms[-1]
            if current_room == dest:
                return movements
            for neighbour_direction, neighbour_room in connections[current_room].items():
                if neighbour_room and neighbour_room not in all_rooms:
                    new_all_rooms = (*all_rooms, neighbour_room)
                    new_movements = (*movements, neighbour_direction)
                    queue.append((new_all_rooms, new_movements))
        raise ValueError(f"could not find path from {source} to {dest}; {connections = }")

    while True:
        places_to_explore = [
            (room, direction)
            for room, room_connections in connections.items()
            for direction, other_room in room_connections.items()
            if not other_room
        ]
        if not places_to_explore:
            break
        room_to_explore_from, direction_to_explore = places_to_explore[0]
        if room_to_explore_from != current_room:
            path = path_from(current_room, room_to_explore_from)
            for movement in path:
                droid.output_queue.clear()
                droid.input_queue.extend([ord(c) for c in movement + "\n"])
                droid.run()
        droid.output_queue.clear()
        droid.input_queue.extend([ord(c) for c in direction_to_explore + "\n"])
        droid.run()
        output_text = "".join(chr(x) for x in droid.output_queue).strip("\n")
        blocks = output_text.split("\n\n")
        room_info = blocks[0]
        new_room = room_info[room_info.index("==") + 3 : room_info.rindex("==") - 1]
        connections[room_to_explore_from][direction_to_explore] = new_room
        connections[new_room][opposite_directions[direction_to_explore]] = room_to_explore_from
        current_room = new_room
        doors = blocks[1]
        for line in doors.split("\n")[1:]:
            door = line[2:]
            if door not in connections[current_room]:
                connections[current_room][door] = ""
        items_in_room = blocks[2]
        if items_in_room.startswith("Items here"):
            for line in items_in_room.split("\n")[1:]:
                item = line[2:]
                if item not in unsafe_items:
                    items.append(item)
                    droid.input_queue.extend([ord(c) for c in f"take {item}\n"])
                    droid.run()
        if current_room == "Pressure-Sensitive Floor":
            current_room = "Security Checkpoint"

    droid.output_queue.clear()
    current_items = set(items)
    move_to_pressure_sensitive_floor = [
        m for m, dest in connections["Security Checkpoint"].items() if dest == "Pressure-Sensitive Floor"
    ][0]
    for item_combination in powerset_of_sets(items):
        items_to_drop = current_items - item_combination
        items_to_pick_up = item_combination - current_items
        current_items = item_combination
        droid.input_queue.extend(ord(c) for c in "".join(f"drop {item}\n" for item in items_to_drop))
        droid.input_queue.extend(ord(c) for c in "".join(f"take {item}\n" for item in items_to_pick_up))
        droid.run()
        droid.output_queue.clear()
        droid.input_queue.extend(ord(c) for c in move_to_pressure_sensitive_floor + "\n")
        droid.run()
        output_text = "".join(chr(x) for x in droid.output_queue)
        if "ejected" not in output_text:
            airlock_password_index = output_text.index("typing") + 7
            print(output_text[airlock_password_index : output_text.index(" ", airlock_password_index)])
            return
