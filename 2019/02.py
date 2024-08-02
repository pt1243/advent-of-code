with open("./2019/resources/2.txt") as f:
    nums = [int(num) for num in f.read().strip().split(",")]


class IntcodeProgram:
    def __init__(self, program: list[int]) -> None:
        self.memory = program
        self.i = 0

    def _add(self) -> None:
        address_1, address_2, target_address = self.memory[self.i + 1 : self.i + 4]
        self.memory[target_address] = self.memory[address_1] + self.memory[address_2]
        self.i += 4

    def _multiply(self) -> None:
        address_1, address_2, target_address = self.memory[self.i + 1 : self.i + 4]
        self.memory[target_address] = self.memory[address_1] * self.memory[address_2]
        self.i += 4

    def run(self) -> None:
        while True:
            opcode = self.memory[self.i]
            if opcode == 1:
                self._add()
            elif opcode == 2:
                self._multiply()
            elif opcode == 99:
                return
            else:
                raise ValueError(f"unknown opcode {opcode}")


def problem_1() -> None:
    nums[1] = 12
    nums[2] = 2
    program = IntcodeProgram(nums)
    program.run()
    print(program.memory[0])


def problem_2() -> None:
    for noun in range(100):
        for verb in range(100):
            program_input = nums.copy()
            program_input[1] = noun
            program_input[2] = verb
            program = IntcodeProgram(program_input)
            program.run()
            if program.memory[0] == 19690720:
                print(100 * noun + verb)
                return
