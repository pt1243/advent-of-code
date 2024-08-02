with open("./2023/resources/6.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    total_product = 1
    for time_str, best_distance_str in zip(lines[0].split()[1:], lines[1].split()[1:]):
        time, best_distance = int(time_str), int(best_distance_str)
        num_wins = 0
        for i in range(time + 1):
            distance = (time - i) * i
            if distance > best_distance:
                num_wins += 1
        total_product *= num_wins
    print(total_product)


def problem_2() -> None:
    time = int("".join(lines[0].split()[1:]))
    best_distance = int("".join(lines[1].split()[1:]))
    num_wins = 0
    for i in range(time + 1):
        distance = (time - i) * i
        if distance > best_distance:
            num_wins += 1
    print(num_wins)
