with open("./2017/resources/19.txt") as f:
    lines = [line.rstrip("\n") for line in f]


def problem_1() -> None:
    num_letters = len([char for row in lines for char in row if char.isupper()])
    row, col = 0, lines[0].index("|")
    direction = "d"
    letters_found = ""
    while True:
        if direction == "d":
            row += 1
        elif direction == "u":
            row -= 1
        elif direction == "l":
            col -= 1
        else:
            col += 1
        char = lines[row][col]
        
        if char.isupper():
            letters_found += char
            if len(letters_found) == num_letters:
                print(letters_found)
                return
        elif char == "+":
            if direction == "d" or direction == "u":
                direction = "l" if col > 0 and not lines[row][col - 1].isspace() else "r"
            else:
                direction = "u" if row > 0 and not lines[row - 1][col].isspace() else "d"


def problem_2() -> None:
    num_letters = len([char for row in lines for char in row if char.isupper()])
    row, col = 0, lines[0].index("|")
    direction = "d"
    letters_found = ""
    steps = 0
    while True:
        steps += 1
        if direction == "d":
            row += 1
        elif direction == "u":
            row -= 1
        elif direction == "l":
            col -= 1
        else:
            col += 1
        char = lines[row][col]
        
        if char.isupper():
            letters_found += char
            if len(letters_found) == num_letters:
                print(steps + 1)
                return
        elif char == "+":
            if direction == "d" or direction == "u":
                direction = "l" if col > 0 and not lines[row][col - 1].isspace() else "r"
            else:
                direction = "u" if row > 0 and not lines[row - 1][col].isspace() else "d"
