from itertools import batched


initial_data = "01110110101001000"


def generate_data(a: str) -> str:
    b = "".join(reversed(a))
    b = b.replace("0", "x").replace("1", "0").replace("x", "1")
    return a + "0" + b


def generate_checksum(data: str) -> str:
    return "".join("1" if c1 == c2 else "0" for c1, c2 in batched(data, 2))


def problem_1() -> None:
    disk_size = 272

    data = initial_data
    while len(data) < disk_size:
        data = generate_data(data)

    data = data[:disk_size]
    checksum = generate_checksum(data)
    while len(checksum) % 2 == 0:
        checksum = generate_checksum(checksum)

    print(checksum)


def problem_2() -> None:
    disk_size = 35651584

    data = initial_data
    while len(data) < disk_size:
        data = generate_data(data)

    data = data[:disk_size]
    checksum = generate_checksum(data)
    while len(checksum) % 2 == 0:
        checksum = generate_checksum(checksum)

    print(checksum)
