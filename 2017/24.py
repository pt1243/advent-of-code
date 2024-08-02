with open("./2017/resources/24.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    components: dict[int, tuple[int, int]] = {}
    for i, line in enumerate(lines):
        left, right = line.split("/")
        components[i] = (int(left), int(right))
    max_strength = 0

    def find_bridges(current_num: int, indices_used: set[int]) -> None:
        nonlocal max_strength
        max_strength = max(max_strength, sum((sum(components[i]) for i in indices_used)))
        next_indices = {i for i, component in components.items() if i not in indices_used and current_num in component}
        for idx in next_indices:
            side_1, side_2 = components[idx]
            next_num = side_2 if side_1 == current_num else side_1
            new_indices = indices_used.copy()
            new_indices.add(idx)
            find_bridges(next_num, new_indices)

    find_bridges(0, set())
    print(max_strength)


def problem_2() -> None:
    components: dict[int, tuple[int, int]] = {}
    for i, line in enumerate(lines):
        left, right = line.split("/")
        components[i] = (int(left), int(right))
    max_strength, max_length = 0, 0

    def find_bridges(current_num: int, indices_used: set[int]) -> None:
        nonlocal max_strength, max_length
        length = len(indices_used)
        if length > max_length:
            max_length = length
            max_strength = sum((sum(components[i]) for i in indices_used))
        elif length == max_length:
            max_strength = max(max_strength, sum((sum(components[i]) for i in indices_used)))
        next_indices = {i for i, component in components.items() if i not in indices_used and current_num in component}
        for idx in next_indices:
            side_1, side_2 = components[idx]
            next_num = side_2 if side_1 == current_num else side_1
            new_indices = indices_used.copy()
            new_indices.add(idx)
            find_bridges(next_num, new_indices)

    find_bridges(0, set())
    print(max_strength)
