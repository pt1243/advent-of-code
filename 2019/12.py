from dataclasses import dataclass
from itertools import combinations, count
from math import lcm

with open("./2019/resources/12.txt") as f:
    lines = f.read().splitlines()


@dataclass
class Moon:
    x: int
    y: int
    z: int
    vx: int
    vy: int
    vz: int


def problem_1() -> None:
    moons: list[Moon] = []
    for line in lines:
        components = line[1:-1].split(", ")
        x, y, z = (int(component[2:]) for component in components)
        moons.append(Moon(x, y, z, 0, 0, 0))

    for _ in range(1000):
        for m1, m2 in combinations(moons, 2):
            if m1.x < m2.x:
                m1.vx += 1
                m2.vx -= 1
            elif m1.x > m2.x:
                m1.vx -= 1
                m2.vx += 1
            if m1.y < m2.y:
                m1.vy += 1
                m2.vy -= 1
            elif m1.y > m2.y:
                m1.vy -= 1
                m2.vy += 1
            if m1.z < m2.z:
                m1.vz += 1
                m2.vz -= 1
            elif m1.z > m2.z:
                m1.vz -= 1
                m2.vz += 1
        for m in moons:
            m.x += m.vx
            m.y += m.vy
            m.z += m.vz

    total_energy = 0
    for m in moons:
        total_energy += (abs(m.x) + abs(m.y) + abs(m.z)) * (abs(m.vx) + abs(m.vy) + abs(m.vz))
    print(total_energy)


def problem_2() -> None:
    moons: list[Moon] = []
    for line in lines:
        components = line[1:-1].split(", ")
        x, y, z = (int(component[2:]) for component in components)
        moons.append(Moon(x, y, z, 0, 0, 0))

    x_seen_states = {tuple((m.x, m.vx) for m in moons)}
    for i in count(1):
        for m1, m2 in combinations(moons, 2):
            if m1.x < m2.x:
                m1.vx += 1
                m2.vx -= 1
            elif m1.x > m2.x:
                m1.vx -= 1
                m2.vx += 1
        for m in moons:
            m.x += m.vx
        tuple_representation = tuple((m.x, m.vx) for m in moons)
        if tuple_representation in x_seen_states:
            x_repeat_length = i
            break
        x_seen_states.add(tuple_representation)

    y_seen_states = {tuple((m.y, m.vy) for m in moons)}
    for i in count(1):
        for m1, m2 in combinations(moons, 2):
            if m1.y < m2.y:
                m1.vy += 1
                m2.vy -= 1
            elif m1.y > m2.y:
                m1.vy -= 1
                m2.vy += 1
        for m in moons:
            m.y += m.vy
        tuple_representation = tuple((m.y, m.vy) for m in moons)
        if tuple_representation in y_seen_states:
            y_repeat_length = i
            break
        y_seen_states.add(tuple_representation)

    z_seen_states = {tuple((m.z, m.vz) for m in moons)}
    for i in count(1):
        for m1, m2 in combinations(moons, 2):
            if m1.z < m2.z:
                m1.vz += 1
                m2.vz -= 1
            elif m1.z > m2.z:
                m1.vz -= 1
                m2.vz += 1
        for m in moons:
            m.z += m.vz
        tuple_representation = tuple((m.z, m.vz) for m in moons)
        if tuple_representation in z_seen_states:
            z_repeat_length = i
            break
        z_seen_states.add(tuple_representation)

    print(lcm(x_repeat_length, y_repeat_length, z_repeat_length))
