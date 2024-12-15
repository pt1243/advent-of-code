with open("./2024/resources/15.txt") as f:
    text = f.read().strip()


def problem_1() -> None:
    grid_lines, moves = text.split("\n\n")
    directions = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}
    walls: set[tuple[int, int]] = set()
    boxes: set[tuple[int, int]] = set()
    robot_row, robot_col = 0, 0
    for row, line in enumerate(grid_lines.split("\n")):
        for col, char in enumerate(line):
            if char == "#":
                walls.add((row, col))
            elif char == "O":
                boxes.add((row, col))
            elif char == "@":
                robot_row, robot_col = row, col

    def get_boxes_to_move(row: int, col: int, drow: int, dcol: int) -> tuple[list[tuple[int, int]], bool]:
        boxes_to_move: list[tuple[int, int]] = []
        while True:
            row += drow
            col += dcol
            if (row, col) in walls:
                return boxes_to_move, False
            if (row, col) not in boxes:
                return boxes_to_move, True
            boxes_to_move.append((row, col))

    for move in moves.replace("\n", ""):
        drow, dcol = directions[move]
        boxes_to_move, robot_can_move = get_boxes_to_move(robot_row, robot_col, drow, dcol)
        if not robot_can_move:
            continue
        for box in reversed(boxes_to_move):
            boxes.remove(box)
            boxes.add((box[0] + drow, box[1] + dcol))
        robot_row += drow
        robot_col += dcol

    print(sum(100 * box[0] + box[1] for box in boxes))


def problem_2() -> None:
    grid_lines, moves = text.split("\n\n")
    directions = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}
    walls: set[tuple[int, int]] = set()
    boxes: set[tuple[int, int]] = set()
    robot_row, robot_col = 0, 0
    for row, line in enumerate(grid_lines.split("\n")):
        for col, char in enumerate(line):
            if char == "#":
                walls.add((row, col * 2))
                walls.add((row, col * 2 + 1))
            elif char == "O":
                boxes.add((row, col * 2))
            elif char == "@":
                robot_row, robot_col = row, col * 2

    def check_can_move_up_down(row: int, col: int, drow: int, boxes_to_move: set[tuple[int, int]]) -> bool:
        if (row + drow, col) in walls or (row + drow, col + 1) in walls:  # wall
            return False  # wall
        if (row + drow, col) not in boxes and (row + drow, col + 1) not in boxes and (row + drow, col - 1) not in boxes:
            return True  # empty
        # otherwise, at least 1 box above: check all positions
        result = True
        if (row + drow, col) in boxes:
            boxes_to_move.add((row + drow, col))
            result &= check_can_move_up_down(row + drow, col, drow, boxes_to_move)
        else:
            if (row + drow, col - 1) in boxes:
                boxes_to_move.add((row + drow, col - 1))
                result &= check_can_move_up_down(row + drow, col - 1, drow, boxes_to_move)
            if (row + drow, col + 1) in boxes:
                boxes_to_move.add((row + drow, col + 1))
                result &= check_can_move_up_down(row + drow, col + 1, drow, boxes_to_move)
        return result

    def get_boxes_to_move(row: int, col: int, drow: int, dcol: int) -> tuple[list[tuple[int, int]], bool]:
        if drow == 0:
            boxes_to_move: list[tuple[int, int]] = []
            while True:
                row += drow
                col += dcol
                if (row, col) in walls:  # hits wall
                    return [], False
                if (row, col - 1) in boxes:  # right side of box, so continue
                    continue
                if (row, col) not in boxes:  # empty space, move
                    return boxes_to_move, True
                boxes_to_move.append((row, col))  # box found
        else:
            # if wall: do not move
            if (row + drow, col) in walls:
                return [], False
            # if no box: just move robot directly
            if (row + drow, col) not in boxes and (row + drow, col - 1) not in boxes:
                return [], True
            boxes_to_move_set: set[tuple[int, int]] = set()
            if (row + drow, col - 1) in boxes:  # robot is on the right side of the box
                can_move = check_can_move_up_down(row, col - 1, drow, boxes_to_move_set)
            else:  # box is on the left side of the box
                can_move = check_can_move_up_down(row, col, drow, boxes_to_move_set)
            return sorted(boxes_to_move_set, reverse=(drow == -1)), can_move

    for move in moves.replace("\n", ""):
        drow, dcol = directions[move]
        boxes_to_move, robot_can_move = get_boxes_to_move(robot_row, robot_col, drow, dcol)
        if not robot_can_move:
            continue
        for box in reversed(boxes_to_move):
            boxes.remove(box)
            boxes.add((box[0] + drow, box[1] + dcol))
        robot_row += drow
        robot_col += dcol

    print(sum(100 * box[0] + box[1] for box in boxes))
