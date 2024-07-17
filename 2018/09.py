from collections import deque


with open("./2018/resources/9.txt") as f:
    words = f.read().strip().split()


def marble_game(num_players: int, highest_num_marble: int) -> int:
    player_scores = {i: 0 for i in range(1, num_players + 1)}
    marble_list = deque([0])
    for marble in range(1, highest_num_marble + 1):
        current_player = (marble - 1) % num_players + 1
        if marble % 23 == 0:
            player_scores[current_player] += marble
            marble_list.rotate(7)
            player_scores[current_player] += marble_list.popleft()
        else:
            marble_list.rotate(-2)
            marble_list.appendleft(marble)
    return max(player_scores.values())


def problem_1() -> None:
    num_players = int(words[0])
    highest_num_marble = int(words[6])
    print(marble_game(num_players, highest_num_marble))


def problem_2() -> None:
    num_players = int(words[0])
    highest_num_marble = int(words[6])
    print(marble_game(num_players, highest_num_marble * 100))
