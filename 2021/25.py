from itertools import count

with open("./2021/resources/25.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    east_sea_cucumbers: set[tuple[int, int]] = set()
    south_sea_cucumbers: set[tuple[int, int]] = set()
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == "v":
                south_sea_cucumbers.add((row, col))
            elif char == ">":
                east_sea_cucumbers.add((row, col))

    width, height = len(lines[0]), len(lines)
    previous_east = east_sea_cucumbers
    previous_south = south_sea_cucumbers

    for step in count(1):
        all_sea_cucumbers = east_sea_cucumbers | south_sea_cucumbers
        east_sea_cucumbers = {
            (row, col) if (row, (col + 1) % width) in all_sea_cucumbers else (row, (col + 1) % width)
            for (row, col) in east_sea_cucumbers
        }
        all_sea_cucumbers = east_sea_cucumbers | south_sea_cucumbers
        south_sea_cucumbers = {
            (row, col) if ((row + 1) % height, col) in all_sea_cucumbers else ((row + 1) % height, col)
            for (row, col) in south_sea_cucumbers
        }

        if previous_east == east_sea_cucumbers and previous_south == south_sea_cucumbers:
            print(step)
            break

        previous_east = east_sea_cucumbers
        previous_south = south_sea_cucumbers
