import heapq


with open("./2024/resources/16.txt") as f:
    lines = f.read().splitlines()


def get_cost(starting_states: list[tuple[int, int, int]], from_end: bool = False) -> dict[tuple[int, int, int], int]:
    directions = ((-1, 0), (0, 1), (1, 0), (0, -1))
    open_set: list[tuple[int, tuple[int, int, int]]] = []
    for state in starting_states:
        heapq.heappush(open_set, (0, state))

    costs: dict[tuple[int, int, int], int] = {}
    while open_set:
        cost, current = heapq.heappop(open_set)
        if current in costs:
            continue
        costs[current] = cost
        row, col, direction = current
        heapq.heappush(open_set, (cost + 1000, (row, col, (direction + 1) % 4)))
        heapq.heappush(open_set, (cost + 1000, (row, col, (direction - 1) % 4)))
        drow, dcol = directions[(direction + 2) % 4 if from_end else direction]
        if lines[row + drow][col + dcol] != "#":
            heapq.heappush(open_set, (cost + 1, (row + drow, col + dcol, direction)))
    return costs


def problem_1() -> None:
    start_row = next(i for i, line in enumerate(lines) if "S" in line)
    start_col = lines[start_row].index("S")
    end_row = next(i for i, line in enumerate(lines) if "E" in line)
    end_col = lines[end_row].index("E")
    costs_from_start = get_cost([(start_row, start_col, 1)])
    print(min(cost for state, cost in costs_from_start.items() if state[0] == end_row and state[1] == end_col))


def problem_2() -> None:
    start_row = next(i for i, line in enumerate(lines) if "S" in line)
    start_col = lines[start_row].index("S")
    end_row = next(i for i, line in enumerate(lines) if "E" in line)
    end_col = lines[end_row].index("E")
    costs_from_start = get_cost([(start_row, start_col, 1)])
    best_cost = min(cost for state, cost in costs_from_start.items() if state[0] == end_row and state[1] == end_col)
    costs_to_end = get_cost([(end_row, end_col, i) for i in range(4)], from_end=True)

    tiles_on_best_path: set[tuple[int, int]] = set()
    for row in range(len(lines)):
        for col in range(len(lines[0])):
            if lines[row][col] == "#":
                continue
            for i in range(4):
                point = (row, col, i)
                if (
                    point in costs_from_start
                    and point in costs_to_end
                    and costs_from_start[point] + costs_to_end[point] == best_cost
                ):
                    tiles_on_best_path.add((row, col))
    print(len(tiles_on_best_path))
