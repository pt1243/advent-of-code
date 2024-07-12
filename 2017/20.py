import numpy as np


with open("./2017/resources/20.txt") as f:
    lines = [line.strip() for line in f]


def problem_1() -> None:
    stupidly_high_number = 1_000_000_000_000_000_000_000
    closest_dist, closest_particle = np.inf, 0
    for i, line in enumerate(lines):
        p_entries, v_entries, a_entries = line.split(", ")
        p_arr = np.array([int(i) for i in p_entries[3:-1].split(",")])
        v_arr = np.array([int(i) for i in v_entries[3:-1].split(",")])
        a_arr = np.array([int(i) for i in a_entries[3:-1].split(",")])

        final_pos = (
            p_arr + stupidly_high_number * v_arr + (stupidly_high_number * (stupidly_high_number + 1) // 2) * a_arr
        )
        final_dist = np.sum(np.abs(final_pos))
        if final_dist < closest_dist:
            closest_dist, closest_particle = final_dist, i
    print(closest_particle)


def problem_2() -> None:
    particles = np.empty((len(lines), 9), dtype=int)
    for i, line in enumerate(lines):
        p_entries, v_entries, a_entries = line.split(", ")
        p_arr = np.array([int(i) for i in p_entries[3:-1].split(",")])
        v_arr = np.array([int(i) for i in v_entries[3:-1].split(",")])
        a_arr = np.array([int(i) for i in a_entries[3:-1].split(",")])
        particles[i, :] = np.block([p_arr, v_arr, a_arr])

    ticks_to_simulate = 200
    for _ in range(ticks_to_simulate):
        particles[:, 3:6] += particles[:, 6:]
        particles[:, :3] += particles[:, 3:6]

        _, unique_indices, counts = np.unique(particles[:, :3], axis=0, return_index=True, return_counts=True)
        if unique_indices.shape[0] != particles.shape[0]:
            indices = unique_indices[counts == 1]
            particles = particles[indices, :]
    print(particles.shape[0])
