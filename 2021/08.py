from collections import defaultdict

with open("./2021/resources/8.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    appearances = 0
    for line in lines:
        outputs = line.split(" | ")[1].split()
        appearances += sum(len(output) in {2, 4, 3, 7} for output in outputs)
    print(appearances)


def problem_2() -> None:
    total = 0
    digit_outputs = {
        frozenset({"a", "b", "c", "e", "f", "g"}): "0",
        frozenset({"c", "f"}): "1",
        frozenset({"a", "c", "d", "e", "g"}): "2",
        frozenset({"a", "c", "d", "f", "g"}): "3",
        frozenset({"b", "c", "d", "f"}): "4",
        frozenset({"a", "b", "d", "f", "g"}): "5",
        frozenset({"a", "b", "d", "e", "f", "g"}): "6",
        frozenset({"a", "c", "f"}): "7",
        frozenset({"a", "b", "c", "d", "e", "f", "g"}): "8",
        frozenset({"a", "b", "c", "d", "f", "g"}): "9",
    }
    for line in lines:
        left, right = line.split(" | ")
        combinations: defaultdict[int, list[set[str]]] = defaultdict(list)
        for input_combo in left.split():
            letters = set(input_combo)
            combinations[len(letters)].append(letters)
        one = combinations[2][0]
        seven = combinations[3][0]
        four = combinations[4][0]
        eight = combinations[7][0]
        six_nine_zero = combinations[6][0] & combinations[6][1] & combinations[6][2]

        a = (seven - one).pop()
        f = (combinations[6][0] & combinations[6][1] & combinations[6][2] & one).pop()
        cf = four & seven
        c = (cf - {f}).pop()
        bd = four - seven
        b = (bd & six_nine_zero).pop()
        d = (bd - {b}).pop()
        g = (six_nine_zero - {a, b, f}).pop()
        e = (eight - {a, b, c, d, f, g}).pop()

        signal_wire_to_segment = {a: "a", b: "b", c: "c", d: "d", e: "e", f: "f", g: "g"}
        output_number = ""
        for output_digit in right.split():
            segments = frozenset({signal_wire_to_segment[char] for char in output_digit})
            output_number += digit_outputs[segments]
        total += int(output_number)
    print(total)
