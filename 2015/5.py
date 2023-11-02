from string import ascii_lowercase


with open('./2015/resources/5.txt') as f:
    strings = [line.strip() for line in f]


def problem_1():
    total = 0
    for s in strings:
        vowel_count = s.count("a") + s.count("e") + s.count("i") + s.count("o") + s.count("u")
        twice_in_a_row = False
        for idx, char in enumerate(s):
            if idx == 0:
                continue
            if char == s[idx - 1]:
                twice_in_a_row = True
                break
        forbidden = any(forbidden_string in s for forbidden_string in ("ab", "cd", "pq", "xy"))
        if vowel_count >= 3 and twice_in_a_row and not forbidden:
            total += 1
    print(total)


def problem_2():
    total = 0
    for s in strings:
        pair_found = False
        for first_idx, first_char in enumerate(s):
            if first_idx == 0:
                continue
            for second_idx, second_char in enumerate(s):
                if second_idx == 0:
                    continue
                if abs(second_idx - first_idx) < 2:  # overlapping
                    continue
                
                if first_char == second_char and s[first_idx-1] == s[second_idx-1]:
                    pair_found = True
                    break
            if pair_found:
                break
        
        three_found = any(c1 + c2 + c1 in s for c1 in ascii_lowercase for c2 in ascii_lowercase)

        if pair_found and three_found:
            total += 1
    print(total)
