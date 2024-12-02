from more_itertools import sliding_window


with open("./2016/resources/7.txt") as f:
    ips = f.read().splitlines()


def problem_1() -> None:
    count = 0

    for ip in ips:
        in_hypernet_sequence = False
        found_abba = False
        found_abba_in_hypernet_sequence = False
        for c1, c2, c3, c4 in sliding_window(ip, 4):
            if c1 == "[":
                in_hypernet_sequence = True
                continue
            if c1 == "]":
                in_hypernet_sequence = False
                continue
            if c1 != c2 and c1 == c4 and c2 == c3:
                if in_hypernet_sequence:
                    found_abba_in_hypernet_sequence = True
                    break
                else:
                    found_abba = True
        if found_abba and not found_abba_in_hypernet_sequence:
            count += 1

    print(count)


def problem_2() -> None:
    count = 0

    for ip in ips:
        in_hypernet_sequence = False
        abas_found: set[str] = set()
        babs_found: set[str] = set()

        for c1, c2, c3 in sliding_window(ip, 3):
            if c1 == "[":
                in_hypernet_sequence = True
                continue
            if c1 == "]":
                in_hypernet_sequence = False
                continue
            if c2 == "[" or c2 == "]" or c3 == "[" or c3 == "]":
                continue
            if c1 == c3 and c2 != c1:
                if in_hypernet_sequence:
                    babs_found.add(c1 + c2 + c3)
                else:
                    abas_found.add(c1 + c2 + c3)

        counted = False
        for aba in abas_found:
            a, b = aba[0], aba[1]
            for bab in babs_found:
                c1, c2, c3 = bab[0], bab[1], bab[2]
                if c1 == b and c2 == a:
                    count += 1
                    counted = True
            if counted:
                break

    print(count)
