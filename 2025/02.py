from itertools import batched

with open("./2025/resources/2.txt") as f:
    text = f.read().strip()


def problem_1() -> None:
    total = 0
    for id_range in text.split(","):
        lower, upper = id_range.split("-")
        for id_number in range(int(lower), int(upper) + 1):
            str_id_number = str(id_number)
            if str_id_number[: len(str_id_number) // 2] == str_id_number[len(str_id_number) // 2 :]:
                total += id_number
    print(total)


def problem_2() -> None:
    total = 0
    for id_range in text.split(","):
        lower, upper = id_range.split("-")
        for id_number in range(int(lower), int(upper) + 1):
            str_id_number = str(id_number)
            for length in range(1, len(str_id_number) // 2 + 1):
                if len(str_id_number) % length == 0 and len(set(batched(str_id_number, length))) == 1:
                    total += id_number
                    break
    print(total)
