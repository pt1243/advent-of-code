import numpy as np

with open("./2020/resources/11.txt") as f:
    lines = f.read().splitlines()


def part_1() -> None:
    height = len(lines)
    width = len(lines[0])
    current_seats = np.array([[0 if char == "." else 1 for char in line] for line in lines])
    while True:
        new_seats = current_seats.copy()
        for row in range(height):
            for col in range(width):
                if current_seats[row, col] == 0:
                    continue
                adjacent_occupied = 0
                if row > 0:
                    if col > 0:
                        adjacent_occupied += current_seats[row - 1, col - 1] == 2
                    adjacent_occupied += current_seats[row - 1, col] == 2
                    if col < width - 1:
                        adjacent_occupied += current_seats[row - 1, col + 1] == 2
                if col > 0:
                    adjacent_occupied += current_seats[row, col - 1] == 2
                if col < width - 1:
                    adjacent_occupied += current_seats[row, col + 1] == 2
                if row < height - 1:
                    if col > 0:
                        adjacent_occupied += current_seats[row + 1, col - 1] == 2
                    adjacent_occupied += current_seats[row + 1, col] == 2
                    if col < width - 1:
                        adjacent_occupied += current_seats[row + 1, col + 1] == 2
                if current_seats[row, col] == 1 and adjacent_occupied == 0:
                    new_seats[row, col] = 2
                elif adjacent_occupied >= 4:
                    new_seats[row, col] = 1
        if np.all(new_seats == current_seats):
            print(np.sum(new_seats == 2))
            return
        current_seats = new_seats


def part_2() -> None:
    height = len(lines)
    width = len(lines[0])
    current_seats = np.array([[0 if char == "." else 1 for char in line] for line in lines])
    seats_visible: dict[tuple[int, int], tuple[tuple[int, int], ...]] = {}
    offsets = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    for row in range(height):
        for col in range(width):
            if current_seats[row, col] == 0:
                continue
            visible: list[tuple[int, int]] = []
            for offset in offsets:
                dist = 1
                found: None | tuple[int, int] = None
                while 0 <= row + dist * offset[0] < height and 0 <= col + dist * offset[1] < width:
                    if current_seats[row + dist * offset[0], col + dist * offset[1]] == 1:
                        found = (row + dist * offset[0], col + dist * offset[1])
                        break
                    dist += 1
                if found is not None:
                    visible.append(found)
            seats_visible[row, col] = tuple(visible)

    while True:
        new_seats = current_seats.copy()
        for row in range(height):
            for col in range(width):
                if current_seats[row, col] == 0:
                    continue
                adjacent_occupied = sum(1 for seat in seats_visible[row, col] if current_seats[seat[0], seat[1]] == 2)
                if current_seats[row, col] == 1 and adjacent_occupied == 0:
                    new_seats[row, col] = 2
                elif adjacent_occupied >= 5:
                    new_seats[row, col] = 1
        if np.all(new_seats == current_seats):
            print(np.sum(new_seats == 2))
            return
        current_seats = new_seats
