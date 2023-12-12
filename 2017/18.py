from collections import defaultdict


with open('./2017/resources/18.txt') as f:
    lines = [line.strip() for line in f]


class Program:
    def __init__(self, instructions: list[str], p: int) -> None:
        self.instructions = instructions
        self.registers: defaultdict[str, int] = defaultdict(int)
        self.registers["p"] = p
        self.i = 0
        self.queue: list[int] = []
        self.send_buffer: int | None = None
        self.running = True
    
    def execute(self) -> None:
        if self.i < 0 or self.i >= len(self.instructions):
            raise ValueError



def problem_1() -> None:
    i = 0
    last_sound = 0
    registers: defaultdict[str, int] = defaultdict(int)
    while 0 <= i < len(lines):
        curr = lines[i]
        split = curr.split()
        if curr.startswith("snd"):
            last_sound = registers[split[1]]
            i += 1
        elif curr.startswith("set"):
            dest, src = split[1], split[2]
            try:
                val = int(src)
            except ValueError:
                val = registers[src]
            registers[dest] = val
            i += 1
        elif curr.startswith("add"):
            dest, src = split[1], split[2]
            try:
                val = int(src)
            except ValueError:
                val = registers[src]
            registers[dest] += val
            i += 1
        elif curr.startswith("mul"):
            dest, src = split[1], split[2]
            try:
                val = int(src)
            except ValueError:
                val = registers[src]
            registers[dest] *= val
            i += 1
        elif curr.startswith("mod"):
            dest, src = split[1], split[2]
            try:
                val = int(src)
            except ValueError:
                val = registers[src]
            registers[dest] %= val
            i += 1
        elif curr.startswith("rcv"):
            condition = split[1]
            if registers[condition] == 0:
                i += 1
                continue
            print(last_sound)
            return
        else:
            condition_src, jump_src = split[1], split[2]
            try:
                condition = int(condition_src)
            except ValueError:
                condition = registers[condition_src]
            if condition <= 0:
                i += 1
                continue
            try:
                jump = int(jump_src)
            except ValueError:
                jump = registers[jump_src]
            i += jump


def problem_2() -> None:
    pass
