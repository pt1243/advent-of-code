from collections import deque
from functools import reduce


with open("./2019/resources/22.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    deck_size = 10007
    cards = deque(range(deck_size))
    for line in lines:
        if line.startswith("cut"):
            num_to_cut = int(line.split()[1])
            cards.rotate(-num_to_cut)
        elif line == "deal into new stack":
            cards.reverse()
        else:
            increment = int(line.split()[-1])
            new_cards = [0 for _ in range(deck_size)]
            for i, card in enumerate(cards):
                new_cards[(i * increment) % deck_size] = card
            cards = deque(new_cards)
    print(cards.index(2019))


def problem_2() -> None:
    deck_size = 119315717514047
    num_shuffles = 101741582076661

    linear_functions: list[tuple[int, int]] = []
    for line in lines:
        if line.startswith("cut"):
            num_to_cut = int(line.split()[1])
            linear_functions.append((1, -num_to_cut))
        elif line == "deal into new stack":
            linear_functions.append((-1, -1))
        else:
            increment = int(line.split()[-1])
            linear_functions.append((increment, 0))

    def compose_linear_functions(f1: tuple[int, int], f2: tuple[int, int]) -> tuple[int, int]:
        a1, b1 = f1
        a2, b2 = f2
        return (a2 * a1) % deck_size, (a2 * b1 + b2) % deck_size

    a, b = reduce(compose_linear_functions, linear_functions)

    # total composition = a^k x + b (1 - a^k)/(1 - a) mod deck_size
    total_a = pow(a, num_shuffles, deck_size)
    total_b = (b * (1 - pow(a, num_shuffles, deck_size)) * pow(1 - a, -1, deck_size)) % deck_size
    # invert the function
    print(((2020 - total_b) * pow(total_a, -1, deck_size)) % deck_size)
