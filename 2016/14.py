from functools import cache
from hashlib import md5
from itertools import count
from more_itertools import sliding_window


with open("./2016/resources/14.txt") as f:
    salt = f.read().strip()


@cache
def hash_salt(i: int) -> str:
    combined = (salt + str(i)).encode()
    return md5(combined).hexdigest()


@cache
def key_stretching(i: int) -> str:
    current = hash_salt(i)
    for _ in range(2016):
        current = md5(current.encode()).hexdigest()
    return current


def problem_1() -> None:
    num_keys_found = 0
    for i in count():
        hex_string = hash_salt(i)
        repeated_char = ""
        for c1, c2, c3 in sliding_window(hex_string, 3):
            if c1 == c2 == c3:
                repeated_char = c1
                break
        if repeated_char:
            search_string = repeated_char * 5
            for j in range(1, 1001):
                new_hex_string = hash_salt(i + j)
                if search_string in new_hex_string:
                    num_keys_found += 1
                    if num_keys_found == 64:
                        print(i)
                        return
                    break


def problem_2() -> None:
    num_keys_found = 0
    for i in count():
        hex_string = key_stretching(i)
        repeated_char = ""
        for c1, c2, c3 in sliding_window(hex_string, 3):
            if c1 == c2 == c3:
                repeated_char = c1
                break
        if repeated_char:
            search_string = repeated_char * 5
            for j in range(1, 1001):
                new_hex_string = key_stretching(i + j)
                if search_string in new_hex_string:
                    num_keys_found += 1
                    if num_keys_found == 64:
                        print(i)
                        return
                    break
