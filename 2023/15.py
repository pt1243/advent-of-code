from typing import NamedTuple

with open("./2023/resources/15.txt") as f:
    strings = f.read().strip().split(",")


def hash_algorithm(s: str) -> int:
    value = 0
    for char in s:
        value += ord(char)
        value *= 17
        value %= 256
    return value


class Lens(NamedTuple):
    label: str
    focal_length: int


def part_1() -> None:
    print(sum(hash_algorithm(s) for s in strings))


def part_2() -> None:
    boxes: dict[int, list[Lens]] = {i: [] for i in range(256)}
    for s in strings:
        if "=" in s:
            label = s[: s.index("=")]
            focal_length = int(s[s.index("=") + 1 :])
            box = boxes[hash_algorithm(label)]
            label_index = next((i for i, lens in enumerate(box) if lens.label == label), None)
            if label_index is not None:
                box[label_index] = Lens(label, focal_length)
            else:
                box.append(Lens(label, focal_length))
        else:
            label = s[:-1]
            box = boxes[hash_algorithm(label)]
            label_index = next((i for i, lens in enumerate(box) if lens.label == label), None)
            if label_index is not None:
                box.pop(label_index)
    print(
        sum(
            (1 + box_num) * i * lens.focal_length
            for box_num, lenses in boxes.items()
            for i, lens in enumerate(lenses, 1)
        )
    )
