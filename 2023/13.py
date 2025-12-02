import numpy as np
import numpy.typing as npt

with open("./2023/resources/13.txt") as f:
    contents = f.read().strip()


def get_reflection_score(arr: npt.NDArray[np.bool_], ignore: tuple[int, int] | None = None) -> tuple[int, int]:
    height, width = arr.shape
    for reflection_left_col in range(width - 1):
        num_to_check = min(reflection_left_col + 1, width - reflection_left_col - 1)
        if all(
            np.all(arr[:, reflection_left_col - i] == arr[:, reflection_left_col + i + 1]) for i in range(num_to_check)
        ):
            result = 1, reflection_left_col + 1
            if result != ignore:
                return result

    for reflection_upper_row in range(height - 1):
        num_to_check = min(reflection_upper_row + 1, height - reflection_upper_row - 1)
        if all(
            np.all(arr[reflection_upper_row - i, :] == arr[reflection_upper_row + i + 1, :])
            for i in range(num_to_check)
        ):
            result = 2, (reflection_upper_row + 1)
            if result != ignore:
                return result

    return 0, 0


def problem_1() -> None:
    total = 0
    for block in contents.split("\n\n"):
        lines = block.strip().split("\n")
        height, width = len(lines), len(lines[0])
        arr = np.zeros((height, width), dtype=bool)
        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                if char == "#":
                    arr[row, col] = True
        score = get_reflection_score(arr)
        total += score[1] if score[0] == 1 else 100 * score[1]

    print(total)


def problem_2() -> None:
    total = 0
    for block in contents.split("\n\n"):
        lines = block.strip().split("\n")
        height, width = len(lines), len(lines[0])
        original_arr = np.zeros((height, width), dtype=bool)
        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                if char == "#":
                    original_arr[row, col] = True
        original_score = get_reflection_score(original_arr)
        found = False
        for row in range(height):
            for col in range(width):
                edited_arr = original_arr.copy()
                edited_arr[row, col] = not edited_arr[row, col]
                score = get_reflection_score(edited_arr, ignore=original_score)
                if score[0] == 0:
                    continue
                total += score[1] if score[0] == 1 else 100 * score[1]
                found = True
                break
            if found:
                break
    print(total)
