with open("./2021/resources/10.txt") as f:
    lines = f.read().splitlines()


def part_1() -> None:
    total_syntax_error_score = 0
    character_pairs = {"(": ")", "[": "]", "{": "}", "<": ">"}
    scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
    for line in lines:
        stack: list[str] = []
        for char in line:
            if char in character_pairs:
                stack.append(char)
            else:
                opening = stack.pop()
                expected = character_pairs[opening]
                if char != expected:
                    total_syntax_error_score += scores[char]
                    break
    print(total_syntax_error_score)


def part_2() -> None:
    completion_scores: list[int] = []
    character_pairs = {"(": ")", "[": "]", "{": "}", "<": ">"}
    scores = {")": 1, "]": 2, "}": 3, ">": 4}
    for line in lines:
        stack: list[str] = []
        for char in line:
            if char in character_pairs:
                stack.append(char)
            else:
                opening = stack.pop()
                expected = character_pairs[opening]
                if char != expected:
                    break
        else:
            score = 0
            while stack:
                score *= 5
                score += scores[character_pairs[stack.pop()]]
            completion_scores.append(score)
    completion_scores.sort()
    print(completion_scores[len(completion_scores) // 2])
