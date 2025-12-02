from collections import defaultdict

with open("./2017/resources/22.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    turn_left = {"u": "l", "l": "d", "d": "r", "r": "u"}
    turn_right = {"u": "r", "r": "d", "d": "l", "l": "u"}
    nodes = defaultdict(bool)
    for i, grid_row in enumerate(lines):
        for j, char in enumerate(grid_row):
            if char == "#":
                nodes[(i, j)] = True
    row = len(lines) // 2
    col = len(lines[0]) // 2
    direction = "u"
    num_caused_infection = 0
    bursts = 10_000
    for _ in range(bursts):
        current_infected = nodes[(row, col)]
        if not current_infected:
            num_caused_infection += 1
        direction = turn_right[direction] if current_infected else turn_left[direction]
        nodes[(row, col)] = False if current_infected else True
        if direction == "u":
            row -= 1
        elif direction == "d":
            row += 1
        elif direction == "l":
            col -= 1
        else:
            col += 1
    print(num_caused_infection)


def problem_2() -> None:
    turn_left = {"u": "l", "l": "d", "d": "r", "r": "u"}
    turn_right = {"u": "r", "r": "d", "d": "l", "l": "u"}
    reverse = {"u": "d", "d": "u", "l": "r", "r": "l"}
    nodes = defaultdict(lambda: 0)
    for i, grid_row in enumerate(lines):
        for j, char in enumerate(grid_row):
            if char == "#":
                nodes[(i, j)] = 2
    row = len(lines) // 2
    col = len(lines[0]) // 2
    direction = "u"
    num_caused_infection = 0
    bursts = 10_000_000
    for _ in range(bursts):
        current_node = nodes[(row, col)]
        if current_node == 0:  # clean
            direction = turn_left[direction]
        elif current_node == 1:  # weakened
            num_caused_infection += 1
        elif current_node == 2:  # infected
            direction = turn_right[direction]
        else:  # flagged
            direction = reverse[direction]
        nodes[(row, col)] = (current_node + 1) % 4
        if direction == "u":
            row -= 1
        elif direction == "d":
            row += 1
        elif direction == "l":
            col -= 1
        else:
            col += 1
    print(num_caused_infection)
