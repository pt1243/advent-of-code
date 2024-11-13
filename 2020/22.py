from collections import deque
from typing import Literal


with open("./2020/resources/22.txt") as f:
    text = f.read().strip()


def problem_1() -> None:
    player_1_deck = deque([int(line) for line in text.split("\n\n")[0].splitlines()[1:]])
    player_2_deck = deque([int(line) for line in text.split("\n\n")[1].splitlines()[1:]])

    while player_1_deck and player_2_deck:
        card_1 = player_1_deck.popleft()
        card_2 = player_2_deck.popleft()
        if card_1 > card_2:
            player_1_deck.append(card_1)
            player_1_deck.append(card_2)
        else:
            player_2_deck.append(card_2)
            player_2_deck.append(card_1)

    winning_deck = player_1_deck if player_1_deck else player_2_deck
    print(sum(i * card for i, card in enumerate(reversed(winning_deck), start=1)))


def problem_2() -> None:
    def play_game_recursive(player_1_deck: deque[int], player_2_deck: deque[int]) -> Literal[1, 2]:
        seen_cards: set[tuple[tuple[int, ...], tuple[int, ...]]] = set()
        while player_1_deck and player_2_deck:
            if (tuple(player_1_deck), tuple(player_2_deck)) in seen_cards:
                return 1
            seen_cards.add((tuple(player_1_deck), tuple(player_2_deck)))

            card_1 = player_1_deck.popleft()
            card_2 = player_2_deck.popleft()

            if len(player_1_deck) >= card_1 and len(player_2_deck) >= card_2:
                winner = play_game_recursive(deque(list(player_1_deck)[:card_1]), deque(list(player_2_deck)[:card_2]))
            else:
                winner = 1 if card_1 > card_2 else 2

            if winner == 1:
                player_1_deck.append(card_1)
                player_1_deck.append(card_2)
            else:
                player_2_deck.append(card_2)
                player_2_deck.append(card_1)

        return 1 if player_1_deck else 2

    player_1_deck = deque([int(line) for line in text.split("\n\n")[0].splitlines()[1:]])
    player_2_deck = deque([int(line) for line in text.split("\n\n")[1].splitlines()[1:]])

    play_game_recursive(player_1_deck, player_2_deck)
    winning_deck = player_1_deck if player_1_deck else player_2_deck
    print(sum(i * card for i, card in enumerate(reversed(winning_deck), start=1)))
