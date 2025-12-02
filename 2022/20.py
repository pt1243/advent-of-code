from __future__ import annotations

with open("./2022/resources/20.txt") as f:
    lines = [int(line) for line in f.read().splitlines()]


class Number:
    def __init__(self, value: int):
        self.value = value
        self.left: Number
        self.right: Number


def create_numbers(lines: list[int]) -> tuple[list[Number], Number]:
    first = Number(lines[0])
    last = first
    numbers = [first]
    zero = first
    for num in lines[1:]:
        new_number = Number(num)
        new_number.left = last
        last.right = new_number
        last = new_number
        numbers.append(new_number)
        if num == 0:
            zero = new_number
    last.right = first
    first.left = last
    return numbers, zero


def mix_numbers(numbers: list[Number]) -> None:
    for number in numbers:
        value = number.value
        if value < 0:
            for _ in range(abs(value) % (len(numbers) - 1)):
                new_left, left, right = number.left.left, number.left, number.right
                new_left.right = number
                number.left, number.right = new_left, left
                left.left, left.right = number, right
                right.left = left
        else:
            for _ in range(value % (len(numbers) - 1)):
                left, right, new_right = number.left, number.right, number.right.right
                left.right = right
                right.left, right.right = left, number
                number.left, number.right = right, new_right
                new_right.left = number


def part_1() -> None:
    numbers, zero = create_numbers(lines)
    mix_numbers(numbers)
    current = zero
    result = 0
    for _ in range(3):
        for _ in range(1000):
            current = current.right
        result += current.value
    print(result)


def part_2() -> None:
    numbers, zero = create_numbers([num * 811589153 for num in lines])
    for _ in range(10):
        mix_numbers(numbers)
    current = zero
    result = 0
    for _ in range(3):
        for _ in range(1000):
            current = current.right
        result += current.value
    print(result)
