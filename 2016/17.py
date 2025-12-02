from collections import deque
from hashlib import md5

with open("./2016/resources/17.txt") as f:
    passcode = f.read().strip()


def problem_1() -> None:
    queue = deque([("", 0, 0)])
    open_chars = ("b", "c", "d", "e", "f")

    while queue:
        path, col, row = queue.popleft()
        if col == 3 and row == 3:
            print(path)
            return
        computed_hash = md5((passcode + path).encode(), usedforsecurity=False).hexdigest()
        if row > 0 and computed_hash[0] in open_chars:
            queue.append((path + "U", col, row - 1))
        if row < 3 and computed_hash[1] in open_chars:
            queue.append((path + "D", col, row + 1))
        if col > 0 and computed_hash[2] in open_chars:
            queue.append((path + "L", col - 1, row))
        if col < 3 and computed_hash[3] in open_chars:
            queue.append((path + "R", col + 1, row))


def problem_2() -> None:
    queue = deque([("", 0, 0)])
    open_chars = ("b", "c", "d", "e", "f")
    max_path = 0

    while queue:
        path, col, row = queue.popleft()
        if col == 3 and row == 3:
            max_path = max(max_path, len(path))
            continue
        computed_hash = md5((passcode + path).encode(), usedforsecurity=False).hexdigest()
        if row > 0 and computed_hash[0] in open_chars:
            queue.append((path + "U", col, row - 1))
        if row < 3 and computed_hash[1] in open_chars:
            queue.append((path + "D", col, row + 1))
        if col > 0 and computed_hash[2] in open_chars:
            queue.append((path + "L", col - 1, row))
        if col < 3 and computed_hash[3] in open_chars:
            queue.append((path + "R", col + 1, row))
    print(max_path)
