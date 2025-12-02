from collections import defaultdict

with open("./2021/resources/12.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    connections: defaultdict[str, list[str]] = defaultdict(list)
    for line in lines:
        left, right = line.split("-")
        connections[left].append(right)
        connections[right].append(left)

    num_paths = 0
    paths_to_explore = [("start", {"start"})]
    while paths_to_explore:
        current_position, seen = paths_to_explore.pop()
        if current_position == "end":
            num_paths += 1
            continue
        for connection in connections[current_position]:
            if connection.islower():
                if connection in seen:
                    continue
                new_seen = seen.copy()
                new_seen.add(connection)
                paths_to_explore.append((connection, new_seen))
            else:
                paths_to_explore.append((connection, seen))
    print(num_paths)


def problem_2() -> None:
    connections: defaultdict[str, list[str]] = defaultdict(list)
    for line in lines:
        left, right = line.split("-")
        connections[left].append(right)
        connections[right].append(left)

    num_paths = 0
    paths_to_explore = [("start", {"start"}, False)]
    while paths_to_explore:
        current_position, seen, visited_twice = paths_to_explore.pop()
        if current_position == "end":
            num_paths += 1
            continue
        for connection in connections[current_position]:
            if connection.islower():
                if connection in seen:
                    if visited_twice or connection == "start":
                        continue
                    paths_to_explore.append((connection, seen, True))
                else:
                    new_seen = seen.copy()
                    new_seen.add(connection)
                    paths_to_explore.append((connection, new_seen, visited_twice))
            else:
                paths_to_explore.append((connection, seen, visited_twice))
    print(num_paths)
