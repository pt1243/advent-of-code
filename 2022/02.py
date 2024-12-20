with open("./2022/resources/2.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    total = 0
    scores = [
        [4, 8, 3],  # rock played; respond with rock, paper, scissors
        [1, 5, 9],  # paper played; respond with rock, paper, scissors
        [7, 2, 6],  # scissors played; respond with rock, paper, scissors
    ]
    for line in lines:
        played, response = line.split()
        total += scores[ord(played) - ord("A")][ord(response) - ord("X")]
    print(total)


def problem_2() -> None:
    total = 0
    scores = [
        [3, 4, 8],  # rock played; lose (scissors), draw (rock), win (paper)
        [1, 5, 9],  # paper played; lose (rock), draw (paper), win (scissors)
        [2, 6, 7],  # scissors played; lose (paper), draw (scissors), win (rock)
    ]
    for line in lines:
        played, response = line.split()
        total += scores[ord(played) - ord("A")][ord(response) - ord("X")]
    print(total)
