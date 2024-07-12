from hashlib import md5
from itertools import count


prefix = "ckczppom"


def problem_1() -> None:
    for i in count(1):
        combined = (prefix + str(i)).encode()
        computed_hash = md5(combined, usedforsecurity=False).hexdigest()
        if computed_hash.startswith("00000"):
            print(i)
            break


def problem_2() -> None:
    for i in count(1):
        combined = (prefix + str(i)).encode()
        computed_hash = md5(combined, usedforsecurity=False).hexdigest()
        if computed_hash.startswith("000000"):
            print(i)
            break
