with open("./2020/resources/5.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    seat_ids = [int(line.replace("F", "0").replace("B", "1").replace("L", "0").replace("R", "1"), 2) for line in lines]
    print(max(seat_ids))


def problem_2() -> None:
    all_seat_ids = {
        int(line.replace("F", "0").replace("B", "1").replace("L", "0").replace("R", "1"), 2) for line in lines
    }
    seat_ids_to_check = set(sorted(all_seat_ids)[1:-1])
    for seat_id in seat_ids_to_check:
        if seat_id - 1 not in all_seat_ids:
            print(seat_id - 1)
            return
        if seat_id + 1 not in all_seat_ids:
            print(seat_id + 1)
            return
