import sys
from typing import List

import numpy as np

from aoc_2023.commons.commons import read_input_to_list


def create_seeds_and_maps(lines: List[str]):
    seeds = []
    maps = {}
    curr_map = {}
    curr_source = ""
    m = 0
    for l in lines:
        if l.startswith("seeds"):
            seeds = [int(s) for s in l.split(":")[1].strip().split()]

        elif "map" in l:
            if len(curr_map) > 0:
                maps.update(curr_map)

            p = l.strip().split()[0].split("-")
            curr_source = p[0]
            curr_target = p[2]
            m = 0
            curr_map = {curr_source: {"target": curr_target, "mappings": {}}}

        elif l == "":
            continue

        else:
            p = [int(s) for s in l.strip().split()]
            assert len(p) == 3
            m += 1
            curr_map[curr_source]["mappings"].update(
                {"m" + str(m): {"source": p[1], "dest": p[0], "length": p[2]}}
            )

    if len(curr_map) > 0:
        maps.update(curr_map)

    return seeds, maps


def get_mapping_value_from(mappings_dict, value) -> int:
    s = mappings_dict["source"]
    d = mappings_dict["dest"]
    l = mappings_dict["length"]

    if s <= value <= s + l - 1:
        return d + (value - s)

    return value


def compute_location_for_s(s, maps) -> int:
    source = "seed"
    n = s
    locations = sys.maxsize
    while True:
        t = maps[source]["target"]
        m = maps[source]["mappings"]
        r = [get_mapping_value_from(m[k], n) for k in m]
        r = [x for x in r if x != n]
        n = r[0] if r else n

        if t == "location":
            if n < locations:
                locations = n
            break

        source = t

    return locations


def part_a(lines: List[str]) -> int:
    seeds, maps = create_seeds_and_maps(lines)
    locations = [compute_location_for_s(s, maps) for s in seeds]

    return np.min(locations)


def part_b(lines: List[str]) -> int:
    seeds, maps = create_seeds_and_maps(lines)
    locations = []
    min_batch_size = 1000
    n_steps = 100  # a too small step size fails because we run into another local minimum

    for i in range(0, len(seeds), 2):
        s_min = seeds[i]
        s_max = seeds[i] + seeds[i + 1]

        while (s_max - s_min) > min_batch_size:
            step_size = int((s_max - s_min) / n_steps)
            ranges = [[s_min + i * step_size, s_min + (i + 1) * step_size] for i in range(n_steps)]
            ranges[-1][1] = s_max
            locs = [
                np.min([compute_location_for_s(r[0], maps), compute_location_for_s(r[1], maps)])
                for r in ranges
            ]
            i = np.argmin(locs)
            s_min = ranges[i][0]
            s_max = ranges[i][1]

        # compute for remaining n seeds
        locations.extend([compute_location_for_s(s, maps) for s in range(s_min, s_max + 1)])

    return np.min(locations)


def run() -> None:
    print("partA:")
    print(part_a(read_input_to_list(__file__)))
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 35

    print("partB:")
    print(part_b(read_input_to_list(__file__)))
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 46

    print("done")
