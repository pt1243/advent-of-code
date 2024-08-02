with open("./2019/resources/1.txt") as f:
    masses = [int(line) for line in f.read().splitlines()]


def problem_1() -> None:
    print(sum((mass // 3) - 2 for mass in masses))


def problem_2() -> None:
    def fuel_required_for(m: int) -> int:
        fuel = (m // 3) - 2
        if fuel > 0:
            fuel += fuel_required_for(fuel)
        return max(fuel, 0)

    print(sum(fuel_required_for(mass) for mass in masses))
