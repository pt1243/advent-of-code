with open("./2016/resources/18.txt") as f:
    first_row = f.read().strip()


def count_safe_tiles(num_rows: int) -> int:
    rows: list[list[bool]] = [[char == "^" for char in first_row]]
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

    return num_rows * row_size - sum(sum(row) for row in rows)


def part_1() -> None:
    print(count_safe_tiles(40))


def part_2() -> None:
    print(count_safe_tiles(400000))
