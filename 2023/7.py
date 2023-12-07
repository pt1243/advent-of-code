from itertools import product


with open('./2023/resources/7.txt') as f:
    lines = [line.strip() for line in f]


def card_to_number(card: str, use_jokers: bool = False) -> int:
    if card == "A":
        return 14
    if card == "K":
        return 13
    if card == "Q":
        return 12
    if card == "J":
        return 11 if not use_jokers else 1
    if card == "T":
        return 10
    return int(card)


def get_hand_type(hand: list[int]) -> int:
    set_cards = set(hand)
    if len(set_cards) == 1:
        return 7  # five of a kind
    if len(set_cards) == 2:
        c1 = hand[0]
        if hand.count(c1) == 1 or hand.count(c1) == 4:
            return 6  # four of a kind
        return 5  # full house
    if len(set_cards) == 3:
        c1, c2, c3 = set_cards
        if hand.count(c1) == 3 or hand.count(c2) == 3 or hand.count(c3) == 3:
            return 4  # three of a kind
        return 3  # two pair
    if len(set_cards) == 4:
        return 2  # one pair
    return 1  # high card


def problem_1() -> None:
    total_winnings = 0
    all_cards: list[tuple[int, tuple[int, int, int, int, int], int]] = []
    for line in lines:
        numbered_cards = [card_to_number(c) for c in line.split()[0]]
        bid = int(line.split()[1])
        hand_type = get_hand_type(numbered_cards)
        all_cards.append((hand_type, tuple(numbered_cards), bid))
    sorted_hands = sorted(all_cards, reverse=True)
    for i, (*_, bid) in enumerate(reversed(sorted_hands), start=1):
        total_winnings += i * bid
    print(total_winnings)


def problem_2() -> None:
    total_winnings = 0
    all_cards: list[tuple[int, tuple[int, int, int, int, int], int]] = []
    for line in lines:
        bid = int(line.split()[1])
        if "J" in line:
            cards = line.split()[0]
            options = [(card_to_number(c),) if c != "J" else tuple(i for i in range(2, 15)) for c in cards]
            possible_hand_types = [get_hand_type(possible_hand) for possible_hand in product(*options)]
            best_hand_type = max(possible_hand_types)
            all_cards.append((best_hand_type, tuple(card_to_number(c, use_jokers=True) for c in cards), bid))
        else:
            numbered_cards = [card_to_number(c) for c in line.split()[0]]
            hand_type = get_hand_type(numbered_cards)
            all_cards.append((hand_type, tuple(numbered_cards), bid))
    sorted_hands = sorted(all_cards, reverse=True)
    for i, (*_, bid) in enumerate(reversed(sorted_hands), start=1):
        total_winnings += i * bid
    print(total_winnings)
