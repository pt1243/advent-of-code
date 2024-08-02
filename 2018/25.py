from dataclasses import dataclass
from typing import cast


with open("./2018/resources/25.txt") as f:
    lines = f.read().splitlines()


@dataclass
class Constellation:
    points: list[tuple[int, int, int, int]]

    def in_range(self, p: tuple[int, int, int, int]) -> bool:
        return any(
            abs(p[0] - point[0]) + abs(p[1] - point[1]) + abs(p[2] - point[2]) + abs(p[3] - point[3]) <= 3
            for point in self.points
        )


def problem_1() -> None:
    points = [cast(tuple[int, int, int, int], tuple((int(x) for x in line.split(",")))) for line in lines]

    constellations: list[Constellation] = []
    for p in points:
        in_range = [c for c in constellations if c.in_range(p)]
        if len(in_range) == 0:
            constellations.append(Constellation([p]))
        elif len(in_range) == 1:
            in_range[0].points.append(p)
        else:
            c1 = in_range[0]
            c1.points.append(p)
            for c2 in in_range[1:]:
                c1.points.extend(c2.points)
                constellations.remove(c2)
    print(len(constellations))
