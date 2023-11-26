from itertools import product


with open('./2015/resources/17.txt') as f:
    sizes = [int(line.strip()) for line in f]


def problem_1() -> None:
    total = 0
    for comb in product((True, False), repeat=len(sizes)):
        comb_total = 0
        for idx, include in enumerate(comb):
            if include:
                comb_total += sizes[idx]
        if comb_total == 150:
            total += 1
    
    print(total)


def problem_2() -> None:
    num_ways = {i: 0 for i in range(len(sizes) + 1)}
    for comb in product((True, False), repeat=len(sizes)):
        comb_total = 0
        for idx, include in enumerate(comb):
            if include:
                comb_total += sizes[idx]
        if comb_total == 150:
             num_ways[sum(comb)] += 1
    
    print(num_ways[min({k: v for k, v in num_ways.items() if v > 0})])
