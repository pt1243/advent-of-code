from typing import cast

import numpy as np
import numpy.typing as npt

with open("./2017/resources/21.txt") as f:
    lines = f.read().splitlines()


def run_iterations(iterations: int) -> int:
    pattern = cast(npt.NDArray[np.bool_], np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1]], dtype=bool))

    two_by_two_inputs: list[npt.NDArray[np.bool_]] = []
    two_by_two_outputs: list[npt.NDArray[np.bool_]] = []
    three_by_three_inputs: list[npt.NDArray[np.bool_]] = []
    three_by_three_outputs: list[npt.NDArray[np.bool_]] = []
    for rule in lines:
        left, right = rule.split(" => ")
        if len(left) == 5:
            target_input, target_output = two_by_two_inputs, two_by_two_outputs
        else:
            target_input, target_output = three_by_three_inputs, three_by_three_outputs
        target_input.append(
            np.array([[1 if char == "#" else 0 for char in row] for row in left.split("/")], dtype=bool)
        )
        target_output.append(
            np.array([[1 if char == "#" else 0 for char in row] for row in right.split("/")], dtype=bool)
        )

    dummy_arr = np.array(0)
    for _ in range(iterations):
        if pattern.shape[0] % 2 == 0:
            skip, input_list, output_list = 2, two_by_two_inputs, two_by_two_outputs
        else:
            skip, input_list, output_list = 3, three_by_three_inputs, three_by_three_outputs
        n = pattern.shape[0] // skip

        new: list[list[npt.NDArray[np.bool_]]] = [[dummy_arr for _ in range(n)] for _ in range(n)]
        cache: dict[tuple[tuple[bool, ...]], npt.NDArray[np.bool_]] = {}
        for i in range(n):
            for j in range(n):
                section = pattern[skip * i : skip * (i + 1), skip * j : skip * (j + 1)]
                section_tuple = cast(tuple[tuple[bool, ...]], tuple(tuple(row) for row in section))
                if section_tuple not in cache:
                    for idx, match in enumerate(input_list):
                        if (
                            np.all(section == match)
                            or np.all(section[:, ::-1] == match)
                            or np.all(section[::-1, :] == match)
                        ):
                            break
                        one_rotation = np.rot90(section)
                        if (
                            np.all(one_rotation == match)
                            or np.all(one_rotation[:, ::-1] == match)
                            or np.all(one_rotation[::-1, :] == match)
                        ):
                            break
                        two_rotations = np.rot90(one_rotation)
                        if np.all(two_rotations == match):
                            break
                        three_rotations = np.rot90(two_rotations)
                        if np.all(three_rotations == match):
                            break
                    cache[section_tuple] = output_list[idx]
                new[i][j] = cache[section_tuple]
        pattern = np.block(new)
    return cast(int, np.sum(pattern))


def problem_1() -> None:
    print(run_iterations(5))


def problem_2() -> None:
    print(run_iterations(18))
