with open("./2020/resources/4.txt") as f:
    text = f.read().strip()


def part_1() -> None:
    required_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
    num_valid = 0
    for passport in text.split("\n\n"):
        fields_present = {entry.split(":")[0] for entry in passport.split()}
        if not required_fields - fields_present:
            num_valid += 1
    print(num_valid)


def part_2() -> None:
    required_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
    num_valid = 0
    for passport in text.split("\n\n"):
        data = {entry.split(":")[0]: entry.split(":")[1] for entry in passport.split()}
        if required_fields - set(data.keys()):
            continue
        if not 1920 <= int(data["byr"]) <= 2002:
            continue
        if not 2010 <= int(data["iyr"]) <= 2020:
            continue
        if not 2020 <= int(data["eyr"]) <= 2030:
            continue
        height_text = data["hgt"]
        if not height_text[:-2]:
            continue
        height = int(height_text[:-2])
        if data["hgt"][-2:] == "cm":
            if not 150 <= height <= 193:
                continue
        elif data["hgt"][-2:] == "in":
            if not 59 <= height <= 76:
                continue
        else:
            continue
        hcl = data["hcl"]
        if not (
            hcl.startswith("#")
            and len(hcl) == 7
            and all(c.isdigit() or c in {"a", "b", "c", "d", "e", "f"} for c in hcl[1:])
        ):
            continue
        if data["ecl"] not in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}:
            continue
        pid = data["pid"]
        if not (len(pid) == 9 and all(c.isdigit() for c in pid)):
            continue
        num_valid += 1
    print(num_valid)
