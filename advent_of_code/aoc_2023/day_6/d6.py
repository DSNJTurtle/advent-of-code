import math
from functools import reduce
from typing import List, Tuple

import numpy as np

from advent_of_code.commons.commons import read_input_to_list


def parse(lines: List[str]) -> List[Tuple[int, int]]:
    times = []
    distances = []
    for l in lines:
        if l.startswith("Time"):
            times = [int(s) for s in l.split(":")[1].strip().split()]
        elif l.startswith("Distance"):
            distances = [int(s) for s in l.split(":")[1].strip().split()]
        else:
            raise RuntimeError("error")

    result = list(zip(times, distances))

    return result


def solve(t, d) -> List[int]:
    """
    Solve quadratic equation d = m*(t-m) for m
    Args:
        t: time
        d: distance

    Returns: (min_m, max_m)

    """
    t_sq = math.pow(t, 2)
    if d > t_sq / 4.0:
        return []
    eps = 1e-6  # needed to shift away from full integers
    max_m = (math.sqrt(t_sq - 4.0 * d) + t) / 2.0
    max_m = int(np.floor(max_m - eps))
    min_m = (t - math.sqrt(t_sq - 4.0 * d)) / 2.0
    min_m = int(np.ceil(min_m + eps))

    return [min_m, max_m]


def part_a(lines: List[str]) -> int:
    td_list = parse(lines)
    wins_per_race = []

    for r in td_list:
        minmax = solve(r[0], r[1])
        wins_per_race.append(minmax[1] - minmax[0] + 1)

    n_wins = reduce(lambda x, y: x * y, wins_per_race)

    return n_wins


def part_b(lines: List[str]) -> int:
    td_list = parse(lines)
    time = int("".join([str(t[0]) for t in td_list]))
    distance = int("".join([str(t[1]) for t in td_list]))
    minmax = solve(time, distance)
    return minmax[1] - minmax[0] + 1


def run() -> None:
    print("partA:")
    print(part_a(read_input_to_list(__file__)))
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 288

    print("partB:")
    print(part_b(read_input_to_list(__file__)))
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 71503

    print("done")
