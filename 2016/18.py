with open('./2016/resources/18.txt') as f:
    first_row = f.read().strip()


def problem_1() -> None:
    num_rows = 40
    rows: list[list[bool]] = [[True if char == "^" else False for char in first_row]]
    row_size = len(rows[0])
    for _ in range(39):
        prev_row = rows[-1]
        new_row: list[bool] = []
        for i, center in enumerate(prev_row):
            left = False if i == 0 else prev_row[i - 1]
            right = False if i == row_size - 1 else prev_row[i + 1]

            if (
                (left and center and not right)
                or (not left and center and right)
                or (left and not center and not right)
                or (not left and not center and right)
            ):
                new_row.append(True)
            else:
                new_row.append(False)
        rows.append(new_row)

    print(num_rows * row_size - sum(sum(row) for row in rows))


def problem_2() -> None:
    num_rows = 400000
    rows: list[list[bool]] = [[True if char == "^" else False for char in first_row]]
    row_size = len(rows[0])
    for _ in range(num_rows - 1):
        prev_row = rows[-1]
        new_row: list[bool] = []
        for i, center in enumerate(prev_row):
            left = False if i == 0 else prev_row[i - 1]
            right = False if i == row_size - 1 else prev_row[i + 1]

            if (
                (left and center and not right)
                or (not left and center and right)
                or (left and not center and not right)
                or (not left and not center and right)
            ):
                new_row.append(True)
            else:
                new_row.append(False)
        rows.append(new_row)

    print(num_rows * row_size - sum(sum(row) for row in rows))
