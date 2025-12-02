with open("./2020/resources/13.txt") as f:
    lines = f.read().splitlines()


def part_1() -> None:
    earliest_arrival = int(lines[0])
    bus_ids = [int(x) for x in lines[1].split(",") if x != "x"]
    multiples: list[int] = []
    for bus_id in bus_ids:
        div, remainder = divmod(earliest_arrival, bus_id)
        multiples.append((div + (remainder != 0)) * bus_id)
    first_time = min(multiples)
    first_bus = bus_ids[multiples.index(first_time)]
    print((first_time - earliest_arrival) * first_bus)


def part_2() -> None:
    remainders_and_moduli = [(int(x) - i, int(x)) for i, x in enumerate(lines[1].split(",")) if x != "x"]

    def extended_euclidian_algorithm(a: int, b: int) -> tuple[int, int]:
        old_r, r = a, b
        old_s, s = 1, 0
        old_t, t = 0, 1
        while r != 0:
            quotient, remainder = divmod(old_r, r)
            if remainder < 0:
                quotient += 1
            old_r, r = r, old_r - quotient * r
            old_s, s = s, old_s - quotient * s
            old_t, t = t, old_t - quotient * t
        return old_s, old_t

    while len(remainders_and_moduli) > 1:
        a1, n1 = remainders_and_moduli[0]
        a2, n2 = remainders_and_moduli[1]
        m1, m2 = extended_euclidian_algorithm(n1, n2)
        x = (a1 * m2 * n2 + a2 * m1 * n1) % (n1 * n2)
        remainders_and_moduli[:2] = [(x, n1 * n2)]

    print(remainders_and_moduli[0][0])
