with open('./2016/resources/7.txt') as f:
    ips = [line.strip() for line in f]


def problem_1() -> None:
    count = 0

    for ip in ips:
        in_hypernet_sequence = False
        found_abba = False
        found_abba_in_hypernet_sequence = False
        for idx, char in enumerate(ip[:-3]):
            if char == "[":
                in_hypernet_sequence = True
                continue
            if char == "]":
                in_hypernet_sequence = False
                continue
            c1, c2, c3, c4 = char, ip[idx + 1], ip[idx + 2], ip[idx + 3]
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

        for idx, char in enumerate(ip[:-2]):
            if char == "[":
                in_hypernet_sequence = True
                continue
            if char == "]":
                in_hypernet_sequence = False
                continue
            c1, c2, c3 = char, ip[idx + 1], ip[idx + 2]
            if c2 == "[" or c2 == "]" or c3 == "[" or c3 == "]":
                continue
            if c1 == c3 and c2 != c1:
                if in_hypernet_sequence:
                    babs_found.add(c1 + c2 + c3)
                else:
                    abas_found.add(c1 + c2 + c3)

        counted = False
        for aba in abas_found:
            (
                a,
                b,
            ) = (
                aba[0],
                aba[1],
            )
            for bab in babs_found:
                c1, c2, c3 = bab[0], bab[1], bab[2]
                if c1 == b and c2 == a:
                    count += 1
                    counted = True
            if counted:
                break

    print(count)
