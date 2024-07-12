from hashlib import md5
from itertools import count

with open("./2016/resources/5.txt") as f:
    door_id = f.read().strip()


def problem_1() -> None:
    password = ""
    for i in count():
        combined = (door_id + str(i)).encode()
        computed_hash = md5(combined, usedforsecurity=False).hexdigest()
        if computed_hash.startswith("00000"):
            password += computed_hash[5]
            if len(password) >= 8:
                print(password)
                break


def problem_2() -> None:
    password: list[None | str] = [None for _ in range(8)]
    for i in count():
        combined = (door_id + str(i)).encode()
        computed_hash = md5(combined, usedforsecurity=False).hexdigest()
        if computed_hash.startswith("00000"):
            position_str = computed_hash[5]
            if position_str.isnumeric():
                position = int(position_str)
                if 0 <= position <= 7 and password[position] is None:
                    password[position] = computed_hash[6]
                    if all(c is not None for c in password):
                        print("".join(password))  # type: ignore[arg-type]
                        break
