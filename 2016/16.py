from itertools import batched

with open("./2016/resources/16.txt") as f:
    initial_data = f.read().strip()


def get_checksum(disk_size: int) -> str:
    data = initial_data
    while len(data) < disk_size:
        b = "".join(reversed(data))
        b = b.replace("0", "x").replace("1", "0").replace("x", "1")
        data += "0" + b
    data = data[:disk_size]

    checksum = "".join("1" if c1 == c2 else "0" for c1, c2 in batched(data, 2))
    while len(checksum) % 2 == 0:
        checksum = "".join("1" if c1 == c2 else "0" for c1, c2 in batched(checksum, 2))
    return checksum


def part_1() -> None:
    print(get_checksum(272))


def part_2() -> None:
    print(get_checksum(35651584))
