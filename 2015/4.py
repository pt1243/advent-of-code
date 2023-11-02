def problem_1():
    from hashlib import md5
    prefix = "ckczppom"
    i = 1
    while True:
        combined = (prefix + str(i)).encode()
        computed_hash = md5(combined, usedforsecurity=False).hexdigest()
        if computed_hash.startswith("00000"):
            print(i)
            break
        i += 1


def problem_2():
    from hashlib import md5
    prefix = "ckczppom"
    i = 1
    while True:
        combined = (prefix + str(i)).encode()
        computed_hash = md5(combined, usedforsecurity=False).hexdigest()
        if computed_hash.startswith("000000"):
            print(i)
            break
        i += 1
