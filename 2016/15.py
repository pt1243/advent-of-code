from itertools import count

with open("./2016/resources/15.txt") as f:
    disc_information_list = f.read().splitlines()


def part_1() -> None:
    discs: dict[int, tuple[int, int]] = {}
    for line in disc_information_list:
        split = line.split()
        discs[int(split[1][1:])] = (int(split[3]), int(split[11][:-1]))

    for i in count():
        if all((initial_pos + i + disc_num) % num_slots == 0 for disc_num, (num_slots, initial_pos) in discs.items()):
            print(i)
            break


def part_2() -> None:
    discs: dict[int, tuple[int, int]] = {}
    for line in disc_information_list:
        split = line.split()
        discs[int(split[1][1:])] = (int(split[3]), int(split[11][:-1]))
    discs[7] = (11, 0)

    for i in count():
        if all((initial_pos + i + disc_num) % num_slots == 0 for disc_num, (num_slots, initial_pos) in discs.items()):
            print(i)
            break
