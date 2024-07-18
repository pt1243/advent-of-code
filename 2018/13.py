from itertools import cycle


with open("./2018/resources/13.txt") as f:
    lines = [line.strip("\n") for line in f]


class Cart:
    movements = ((-1, 0), (0, 1), (1, 0), (0, -1))  # up, right, down, left
    backslash_directions = {1: 2, 0: 3, 3: 0, 2: 1}
    slash_directions = {1: 0, 2: 3, 3: 2, 0: 1}

    def __init__(self, row: int, col: int, direction: int) -> None:
        self.row = row
        self.col = col
        self.direction = direction
        self.turns = cycle([-1, 0, 1])  # left, straight, right
        self.marked_for_removal = False

    def move(self) -> None:
        drow, dcol = self.movements[self.direction]
        self.row += drow
        self.col += dcol

    def change_direction(self, char: str) -> None:
        if char == "\\":
            self.direction = self.backslash_directions[self.direction]
        elif char == "/":
            self.direction = self.slash_directions[self.direction]
        elif char == "+":
            self.direction += next(self.turns)
            self.direction %= 4


def problem_1() -> None:
    carts: list[Cart] = []
    track: list[str] = []
    for row, line in enumerate(lines):
        row_text = ""
        for col, char in enumerate(line):
            if char in ("^", ">", "v", "<"):
                cart = Cart(row, col, ("^", ">", "v", "<").index(char))
                carts.append(cart)
                row_text += "-" if char in (">", "<") else "|"
            else:
                row_text += char
        track.append(row_text)

    while True:
        carts.sort(key=lambda c: (c.row, c.col))
        for cart in carts:
            cart.move()
            char = track[cart.row][cart.col]
            cart.change_direction(char)
            for other_cart in carts:
                if other_cart.row == cart.row and other_cart.col == cart.col and other_cart is not cart:
                    print(f"{cart.col},{cart.row}")
                    return


def problem_2() -> None:
    carts: list[Cart] = []
    track: list[str] = []
    for row, line in enumerate(lines):
        row_text = ""
        for col, char in enumerate(line):
            if char in ("^", ">", "v", "<"):
                cart = Cart(row, col, ("^", ">", "v", "<").index(char))
                carts.append(cart)
                row_text += "-" if char in (">", "<") else "|"
            else:
                row_text += char
        track.append(row_text)

    while True:
        carts.sort(key=lambda c: (c.row, c.col))
        recreate_carts = False
        for cart in carts:
            if cart.marked_for_removal:
                recreate_carts = True
                continue
            cart.move()
            char = track[cart.row][cart.col]
            cart.change_direction(char)
            for other_cart in carts:
                if other_cart.row == cart.row and other_cart.col == cart.col and other_cart is not cart:
                    cart.marked_for_removal = True
                    other_cart.marked_for_removal = True
                    recreate_carts = True
        if recreate_carts:
            carts = [c for c in carts if not c.marked_for_removal]
        if len(carts) == 1:
            print(f"{carts[0].col},{carts[0].row}")
            return
