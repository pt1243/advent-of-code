current_password = "hepxcrrq"


def inc_list(lst: list[int]) -> list[int]:
    lst[-1] += 1
    while any(i > 25 for i in lst):
        last_idx = 0
        for idx, val in enumerate(lst):
            if val > 25:
                last_idx = idx
        lst[last_idx] -= 26
        lst[last_idx-1] += 1
    return lst


def get_next_password(current: str) -> str:
    password = [ord(c) - ord("a") for c in current]
    i_int = ord("i") - ord("a")
    o_int = ord("o") - ord("a")
    l_int = ord("l") - ord("a")

    while True:
        password = inc_list(password)
        if i_int in password or o_int in password or l_int in password:
            continue
        if not any(password[i] + 2 == password[i+1] + 1 == password[i+2] for i in range(6)):
            continue
        pairs_start_indices = [i for i in range(7) if password[i] == password[i+1]]
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


def problem_1() -> None:
    print(get_next_password(current_password))


def problem_2() -> None:
    first = get_next_password(current_password)
    print(get_next_password(first))
