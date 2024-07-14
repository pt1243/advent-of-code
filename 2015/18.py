with open("./2015/resources/18.txt") as f:
    lines = [line.strip() for line in f]


def get_num_neighbours_on(matrix: list[list[bool]], i: int, j: int):
    max_idx = len(matrix) - 1
    above = i > 0
    below = i < max_idx
    left = j > 0
    right = j < max_idx

    num = 0
    if above:
        if left:
            num += matrix[i - 1][j - 1]
        num += matrix[i - 1][j]
        if right:
            num += matrix[i - 1][j + 1]
    if left:
        num += matrix[i][j - 1]
    if right:
        num += matrix[i][j + 1]
    if below:
        if left:
            num += matrix[i + 1][j - 1]
        num += matrix[i + 1][j]
        if right:
            num += matrix[i + 1][j + 1]
    return num


def problem_1() -> None:
    matrix: list[list[bool]] = [[True if char == "#" else False for char in line] for line in lines]
    update_dict: dict[tuple[int, int], bool] = {}

    for _ in range(100):
        for i in range(100):
            for j in range(100):
                light = matrix[i][j]
                neighbours = get_num_neighbours_on(matrix, i, j)
                if light:
                    update_dict[(i, j)] = True if neighbours == 2 or neighbours == 3 else False
                else:
                    update_dict[(i, j)] = True if neighbours == 3 else False
        for i in range(100):
            for j in range(100):
                matrix[i][j] = update_dict[(i, j)]
    print(sum(sum(line) for line in matrix))


def problem_2() -> None:
    matrix: list[list[bool]] = [[True if char == "#" else False for char in line] for line in lines]
    update_dict: dict[tuple[int, int], bool] = {}

    matrix[0][0] = True
    matrix[0][-1] = True
    matrix[-1][0] = True
    matrix[-1][-1] = True

    for _ in range(100):
        for i in range(100):
            for j in range(100):
                light = matrix[i][j]
                neighbours = get_num_neighbours_on(matrix, i, j)
                if light:
                    update_dict[(i, j)] = True if neighbours == 2 or neighbours == 3 else False
                else:
                    update_dict[(i, j)] = True if neighbours == 3 else False
        update_dict[(0, 0)] = True
        update_dict[(0, 99)] = True
        update_dict[(99, 0)] = True
        update_dict[(99, 99)] = True
        for i in range(100):
            for j in range(100):
                matrix[i][j] = update_dict[(i, j)]
    print(sum(sum(line) for line in matrix))
