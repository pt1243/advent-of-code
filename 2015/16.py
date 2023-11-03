import json
from pprint import pprint


with open('./2015/resources/16.txt') as f:
    sues = [line.strip() for line in f]


def problem_1():
    fields = (
        "children",
        "cats",
        "samoyeds",
        "pomeranians",
        "akitas",
        "vizslas",
        "goldfish",
        "trees",
        "cars",
        "perfumes",
    )

    sue_data: dict[int, dict[str, int]] = {i: {f: None for f in fields} for i in range(1, 501)}

    for line in sues:
        sue_name, line_data = line.split(": ", maxsplit=1)
        sue_num = int(sue_name.split()[1])
        for entry in line_data.split(", "):
            field, num = entry.split(": ")
            num = int(num)
            sue_data[sue_num][field] = num

    actual_data = {
        "children": 3,
        "cats": 7,
        "samoyeds": 2,
        "pomeranians": 3,
        "akitas": 0,
        "vizslas": 0,
        "goldfish": 5,
        "trees": 3,
        "cars": 2,
        "perfumes": 1,
    }

    for possible_sue, possible_sue_data in sue_data.items():
        valid = True
        for field, count in actual_data.items():
            if possible_sue_data[field] is None:
                continue
            if possible_sue_data[field] != count:
                valid = False
                break
        if valid:
            print(possible_sue)
            break


def problem_2():
    fields = (
        "children",
        "cats",
        "samoyeds",
        "pomeranians",
        "akitas",
        "vizslas",
        "goldfish",
        "trees",
        "cars",
        "perfumes",
    )

    sue_data: dict[int, dict[str, int]] = {i: {f: None for f in fields} for i in range(1, 501)}

    for line in sues:
        sue_name, line_data = line.split(": ", maxsplit=1)
        sue_num = int(sue_name.split()[1])
        for entry in line_data.split(", "):
            field, num = entry.split(": ")
            num = int(num)
            sue_data[sue_num][field] = num

    actual_data = {
        "children": 3,
        "cats": 7,
        "samoyeds": 2,
        "pomeranians": 3,
        "akitas": 0,
        "vizslas": 0,
        "goldfish": 5,
        "trees": 3,
        "cars": 2,
        "perfumes": 1,
    }

    for possible_sue, possible_sue_data in sue_data.items():
        valid = True
        for field, count in actual_data.items():
            if possible_sue_data[field] is None:
                continue
            if field == "cats" or field == "trees":
                if possible_sue_data[field] <= count:
                    valid = False
            elif field == "pomeranians" or field == "goldfish":
                if possible_sue_data[field] >= count:
                    valid = False
            elif possible_sue_data[field] != count:
                valid = False
            if not valid:
                break
        if valid:
            print(possible_sue)
            break
