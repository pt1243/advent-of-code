from collections.abc import Iterable
from itertools import cycle


with open('./2015/resources/14.txt') as f:
    lines = [line.strip() for line in f]


def problem_1():
    all_reindeer: dict[str, Iterable] = {}
    for line in lines:
        reindeer = line.split(maxsplit=1)[0]
        speed = int(line[line.index("fly")+4:line.index("km/s")-1])
        flying_time = int(line[line.index("for")+4:line.index("seconds")-1])
        rest_time = int(line[line.rindex("for")+4:line.rindex("seconds")-1])
        lst = [speed for _ in range(flying_time)] + [0 for _ in range(rest_time)]
        all_reindeer[reindeer] = cycle(lst)
    
    distances = {r: 0 for r in all_reindeer}
    for _ in range(1000):
        for reindeer, iterator in all_reindeer.items():
            distances[reindeer] += next(iterator)
    
    print(max(distances.values()))


def problem_2():
    all_reindeer: dict[str, Iterable] = {}
    for line in lines:
        reindeer = line.split(maxsplit=1)[0]
        speed = int(line[line.index("fly")+4:line.index("km/s")-1])
        flying_time = int(line[line.index("for")+4:line.index("seconds")-1])
        rest_time = int(line[line.rindex("for")+4:line.rindex("seconds")-1])
        lst = [speed for _ in range(flying_time)] + [0 for _ in range(rest_time)]
        all_reindeer[reindeer] = cycle(lst)
    
    distances = {r: 0 for r in all_reindeer}
    points = {r: 0 for r in all_reindeer}
    for _ in range(2503):
        for reindeer, iterator in all_reindeer.items():
            distances[reindeer] += next(iterator)
        for reindeer in points:
            if distances[reindeer] == max(distances.values()):
                points[reindeer] += 1
    
    winning_reindeer = [r for r, p in points.items() if p == max(points.values())][0]
    print(points[winning_reindeer])
