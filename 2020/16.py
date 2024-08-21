from copy import deepcopy
from math import prod


with open("./2020/resources/16.txt") as f:
    text = f.read().strip()


def problem_1() -> None:
    rules, _, nearby_tickets = text.split("\n\n")
    allowable_ranges: list[tuple[int, int, int, int]] = []
    for rule_text in rules.split("\n"):
        left_range, right_range = rule_text.split(": ")[1].split(" or ")
        val_1, val_2 = (int(x) for x in left_range.split("-"))
        val_3, val_4 = (int(x) for x in right_range.split("-"))
        allowable_ranges.append((val_1, val_2, val_3, val_4))

    ticket_scanning_error_rate = 0
    for ticket in nearby_tickets.split("\n")[1:]:
        fields = [int(num) for num in ticket.split(",")]
        for field in fields:
            if not any(rule[0] <= field <= rule[1] or rule[2] <= field <= rule[3] for rule in allowable_ranges):
                ticket_scanning_error_rate += field
                break
    print(ticket_scanning_error_rate)


def problem_2() -> None:
    rules, ticket, nearby_tickets = text.split("\n\n")
    allowable_ranges: list[tuple[int, int, int, int]] = []
    for rule_text in rules.split("\n"):
        left_range, right_range = rule_text.split(": ")[1].split(" or ")
        val_1, val_2 = (int(x) for x in left_range.split("-"))
        val_3, val_4 = (int(x) for x in right_range.split("-"))
        allowable_ranges.append((val_1, val_2, val_3, val_4))
    possible_correspondences = [set(range(len(allowable_ranges))) for _ in range(len(allowable_ranges))]

    valid_tickets: list[list[int]] = []
    for nearby_ticket in nearby_tickets.split("\n")[1:]:
        fields = [int(num) for num in nearby_ticket.split(",")]
        for field in fields:
            if not any(rule[0] <= field <= rule[1] or rule[2] <= field <= rule[3] for rule in allowable_ranges):
                break
        else:
            valid_tickets.append(fields)

    for fields in valid_tickets:
        for field, correspondence in zip(fields, possible_correspondences):
            for i, rule in enumerate(allowable_ranges):
                if not (rule[0] <= field <= rule[1] or rule[2] <= field <= rule[3]):
                    correspondence.discard(i)

    while any(len(c) > 1 for c in possible_correspondences):
        new_correspondences = deepcopy(possible_correspondences)
        for i, c in enumerate(possible_correspondences):
            if len(c) == 1:
                item_to_remove = c.pop()
                for j, new_c in enumerate(new_correspondences):
                    if i == j:
                        continue
                    new_c.discard(item_to_remove)
        possible_correspondences = new_correspondences

    mapping = {c.pop(): i for i, c in enumerate(possible_correspondences)}
    departure_indices = [i for i, rule in enumerate(rules.split("\n")) if rule.startswith("departure")]
    ticket_fields = [int(x) for x in ticket.split("\n")[1].split(",")]

    print(prod(ticket_fields[mapping[i]] for i in departure_indices))
