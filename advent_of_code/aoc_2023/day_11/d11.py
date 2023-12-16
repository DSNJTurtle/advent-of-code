from typing import List

import numpy as np

from advent_of_code.commons.commons import read_input_to_list


def parse_matrix(lines: List[str], galaxy_offset=10):
    m = []
    next_galaxy = galaxy_offset
    for l in lines:
        mm = []
        for ll in l:
            if ll == ".":
                mm.append(1)
            else:
                mm.append(next_galaxy)
                next_galaxy += 1

        m.append(mm)

    m = np.array(m)
    d = {"rows": [], "cols": []}
    for i in range(len(m)):
        if np.all(m[i] < galaxy_offset):
            d["rows"].append(i)

    for j in range(len(m[0])):
        if np.all(m[:, j] < galaxy_offset):
            d["cols"].append(j)

    return m, d


def get_galaxies(m, galaxy_offset):
    indices_of_galaxies = list(zip(*np.where(m >= galaxy_offset)))
    positions = {m[i, j] - galaxy_offset + 1: (i, j) for i, j in indices_of_galaxies}
    return positions


def shortest_paths_with_multiplier(galaxies, m, d, multiplier):
    sum_length = 0
    for g1 in galaxies:
        xi, xj = galaxies[g1]
        for g2 in [k for k in galaxies if k > g1]:
            yi, yj = galaxies[g2]
            n_rows_in_range = len(list(filter(lambda x: min(xi, yi) < x < max(xi, yi), d["rows"])))
            n_cols_in_range = len(list(filter(lambda x: min(xj, yj) < x < max(xj, yj), d["cols"])))
            sum_length += (
                abs(xi - yi)
                + abs(xj - yj)
                + n_rows_in_range * (multiplier - 1)
                + n_cols_in_range * (multiplier - 1)
            )

    return sum_length


def part_a(lines: List[str]) -> int:
    galaxy_offset = 10
    m, d = parse_matrix(lines, galaxy_offset)
    galaxies = get_galaxies(m, galaxy_offset)
    return shortest_paths_with_multiplier(galaxies, m, d, 2)


def part_b(lines: List[str], multiplier: int) -> int:
    galaxy_offset = 10
    m, d = parse_matrix(lines, galaxy_offset)
    galaxies = get_galaxies(m, galaxy_offset)
    return shortest_paths_with_multiplier(galaxies, m, d, multiplier)


def run() -> None:
    print("partA:")
    assert part_a(read_input_to_list(__file__)) == 10228230
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 374

    print("partB:")
    assert part_b(read_input_to_list(__file__), multiplier=1000000) == 447073334102
    assert part_b(read_input_to_list(__file__, read_test_input=True), multiplier=10) == 1030
    assert part_b(read_input_to_list(__file__, read_test_input=True), multiplier=100) == 8410

    print("done")
