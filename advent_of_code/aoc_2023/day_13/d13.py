from __future__ import annotations

from typing import List

import numpy as np

from advent_of_code.commons.commons import read_input_to_list


def parse(lines: List[str]):
    patterns = []
    pattern = []
    for l in lines:
        if l == "":
            patterns.append(np.array(pattern))
            pattern = []
        else:
            pattern.append([int(s) for s in l.replace(".", "0").replace("#", "1")])

    # last pattern
    patterns.append(np.array(pattern))

    return patterns


def find_vertical_reflection(p, margin: int):
    _sum = 0
    for from_col in range(1, len(p[0])):
        max_dist_to_end = min(from_col, len(p[0]) - from_col)
        left = p[:, from_col - max_dist_to_end : from_col]
        right = p[:, from_col : from_col + max_dist_to_end]
        assert (len(left[0]) + len(right[0])) % 2 == 0
        if np.count_nonzero(left != np.flip(right, axis=1)) == margin:
            _sum += from_col

    return _sum


def part_a(lines: List[str]) -> int:
    patterns = parse(lines)

    s = 0
    for i, p in enumerate(patterns):
        s += find_vertical_reflection(p, 0)
        s += 100 * find_vertical_reflection(np.transpose(p), 0)

    return s


def part_b(lines: List[str]) -> int:
    patterns = parse(lines)

    s = 0
    for i, p in enumerate(patterns):
        s += find_vertical_reflection(p, 1)
        s += 100 * find_vertical_reflection(np.transpose(p), 1)

    return s


def run() -> None:
    print("partA:")
    assert part_a(read_input_to_list(__file__)) == 28895
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 405

    print("partB:")
    assert part_b(read_input_to_list(__file__)) == 31603
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 400

    print("done")
