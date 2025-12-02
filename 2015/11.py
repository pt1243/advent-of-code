with open("./2015/resources/11.txt") as f:
    current_password = f.read().strip()


def get_next_password(current: str) -> str:
    password = [ord(c) - ord("a") for c in current]
    i_int = ord("i") - ord("a")
    o_int = ord("o") - ord("a")
    l_int = ord("l") - ord("a")

    while True:
        password[-1] += 1
        for i in range(7, 0, -1):
            if password[i] == 26:
                password[i - 1] += 1
                password[i] = 0

        if i_int in password or o_int in password or l_int in password:
            continue
        if not any(password[i] + 2 == password[i + 1] + 1 == password[i + 2] for i in range(6)):
            continue
        pairs_start_indices = [i for i in range(7) if password[i] == password[i + 1]]
        pairs_found = False
        for first_index in pairs_start_indices:
            for second_index in pairs_start_indices:
                if abs(first_index - second_index) < 2:
                    continue
                if password[first_index] != password[second_index]:
                    pairs_found = True
                    break
            if pairs_found:
                break
        if pairs_found:
            return "".join(chr(c + ord("a")) for c in password)


def part_1() -> None:
    print(get_next_password(current_password))


def part_2() -> None:
    first = get_next_password(current_password)
    print(get_next_password(first))
