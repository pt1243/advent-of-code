import numpy as np

with open("./2021/resources/4.txt") as f:
    text = f.read().strip().split("\n\n")


def part_1() -> None:
    numbers = [int(x) for x in text[0].split(",")]
    boards = np.array([[[int(x) for x in line.split()] for line in board.split("\n")] for board in text[1:]], int)
    filled = np.zeros_like(boards, bool)

    for num in numbers:
        filled = filled | (boards == num)
        row_sums = np.sum(filled, axis=2)
        column_sums = np.sum(filled, axis=1)
        if np.any(row_sums == 5):
            winning_board = np.where(row_sums == 5)[0]
            break
        if np.any(column_sums == 5):
            winning_board = np.where(column_sums == 5)[0]
            break
    score = np.sum(boards[winning_board][np.invert(filled[winning_board])])
    print(score * num)


def part_2() -> None:
    numbers = [int(x) for x in text[0].split(",")]
    boards = np.array([[[int(x) for x in line.split()] for line in board.split("\n")] for board in text[1:]], int)
    filled = np.zeros_like(boards, bool)
    completed = np.zeros(boards.shape[0], bool)

    on_last_board = False
    for num in numbers:
        filled = filled | (boards == num)
        row_sums = np.sum(filled, axis=2)
        column_sums = np.sum(filled, axis=1)
        completed = completed | np.any(row_sums == 5, axis=1) | np.any(column_sums == 5, axis=1)
        if on_last_board and np.sum(np.invert(completed)) == 0:
            break
        if np.sum(np.invert(completed)) == 1:
            on_last_board = True
            last_winning_board = np.argmin(completed)
            continue
    score = np.sum(boards[last_winning_board][np.invert(filled[last_winning_board])])
    print(score * num)
