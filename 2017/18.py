from collections import defaultdict

with open("./2017/resources/18.txt") as f:
    lines = f.read().splitlines()


class AsyncProgram:
    def __init__(self, instructions: list[str], p: int) -> None:
        self.instructions = instructions
        self.registers: defaultdict[str, int] = defaultdict(int)
        self.registers["p"] = p
        self.i = 0
        self.receive_queue: list[int] = []
        self.send_queue: list[int] = []
        self.times_value_sent = 0

    def execute(self) -> None:
        if self.i < 0 or self.i >= len(self.instructions):
            return
        while 0 <= self.i < len(lines):
            curr = self.instructions[self.i]
            split = curr.split()
            if curr.startswith("set"):
                dest, src = split[1], split[2]
                try:
                    val = int(src)
                except ValueError:
                    val = self.registers[src]
                self.registers[dest] = val
                self.i += 1
            elif curr.startswith("add"):
                dest, src = split[1], split[2]
                try:
                    val = int(src)
                except ValueError:
                    val = self.registers[src]
                self.registers[dest] += val
                self.i += 1
            elif curr.startswith("mul"):
                dest, src = split[1], split[2]
                try:
                    val = int(src)
                except ValueError:
                    val = self.registers[src]
                self.registers[dest] *= val
                self.i += 1
            elif curr.startswith("mod"):
                dest, src = split[1], split[2]
                try:
                    val = int(src)
                except ValueError:
                    val = self.registers[src]
                self.registers[dest] %= val
                self.i += 1
            elif curr.startswith("jgz"):
                condition_src, jump_src = split[1], split[2]
                try:
                    condition = int(condition_src)
                except ValueError:
                    condition = self.registers[condition_src]
                if condition <= 0:
                    self.i += 1
                    continue
                try:
                    jump = int(jump_src)
                except ValueError:
                    jump = self.registers[jump_src]
                self.i += jump
            elif curr.startswith("snd"):
                try:
                    val = int(split[1])
                except ValueError:
                    val = self.registers[split[1]]
                self.send_queue.append(val)
                self.times_value_sent += 1
                self.i += 1
            elif curr.startswith("rcv"):
                if not self.receive_queue:
                    return
                self.registers[split[1]] = self.receive_queue.pop(0)
                self.i += 1
            else:
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
            reg = split[1]
            if registers[reg] == 0:
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
    p0 = AsyncProgram(lines, 0)
    p1 = AsyncProgram(lines, 1)
    while True:
        p0.execute()
        p1.receive_queue += p0.send_queue
        p0.send_queue = []
        p1.execute()
        p0.receive_queue += p1.send_queue
        p1.send_queue = []
        if not p0.send_queue and not p0.receive_queue and not p1.send_queue and not p1.receive_queue:
            break
    print(p1.times_value_sent)
