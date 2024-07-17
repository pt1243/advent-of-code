from collections import defaultdict

import numpy as np


with open("./2018/resources/3.txt") as f:
    lines = [line.strip() for line in f]


def problem_1() -> None:
    fabric = np.zeros((1000, 1000), dtype=int)
    for claim in lines:
        _, positions = claim.split(" @ ")
        distances, dimensions = positions.split(": ")
        left_distance, top_distance = int(distances.split(",")[0]), int(distances.split(",")[1])
        width, height = int(dimensions.split("x")[0]), int(dimensions.split("x")[1])
        fabric[top_distance : top_distance + height, left_distance : left_distance + width] += 1
    print(np.sum(fabric >= 2))


def problem_2() -> None:
    claims_made: defaultdict[tuple[int, int], list[int]] = defaultdict(list)
    for claim in lines:
        claim_id, positions = claim.split(" @ ")
        claim_number = int(claim_id[1:])
        distances, dimensions = positions.split(": ")
        left_distance, top_distance = int(distances.split(",")[0]), int(distances.split(",")[1])
        width, height = int(dimensions.split("x")[0]), int(dimensions.split("x")[1])
        for row in range(top_distance, top_distance + height):
            for col in range(left_distance, left_distance + width):
                claims_made[(row, col)].append(claim_number)

    for claim in lines:
        claim_id, positions = claim.split(" @ ")
        claim_number = int(claim_id[1:])
        distances, dimensions = positions.split(": ")
        left_distance, top_distance = int(distances.split(",")[0]), int(distances.split(",")[1])
        width, height = int(dimensions.split("x")[0]), int(dimensions.split("x")[1])
        single_claim_list = [claim_number]
        if all(
            claims_made[(row, col)] == single_claim_list
            for row in range(top_distance, top_distance + height)
            for col in range(left_distance, left_distance + width)
        ):
            print(claim_number)
            return
