from __future__ import annotations

from typing import List

import numpy as np

from advent_of_code.commons.commons import read_input_to_list


def parse(lines: List[str]):
    d = {"R": 1j, "L": -1j, "U": complex(1, 0), "D": complex(-1, 0)}
    _input = []
    for l in lines:
        p = l.split()
        direction = d[p[0].strip()]
        steps = int(p[1].strip())
        color = p[2].replace("#", "").replace("(", "").replace(")", "").strip()

        _input.append((direction, steps, color))

    return _input


def parse_b(lines: List[str]):
    d = {0: 1j, 2: -1j, 3: complex(1, 0), 1: complex(-1, 0)}
    _input = []
    for l in lines:
        p = l.split()
        color = p[2].replace("#", "").replace("(", "").replace(")", "").strip()
        steps = int(color[:-1], 16)
        direction = d[int(color[-1])]

        _input.append((direction, steps, color))

    return _input


def compute_polygon_area(_input):
    # adapted from https://en.wikipedia.org/wiki/Shoelace_formula
    steps = [(d, l) for d, l, _ in _input]
    pos = complex(0, 0)
    area = 0
    sum_steps = 0
    while steps:
        next_dir, next_l = steps.pop(0)
        sum_steps += next_l
        next_pos = pos + next_l * next_dir
        area += np.linalg.det(np.array([[pos.real, next_pos.real], [pos.imag, next_pos.imag]]))
        pos = next_pos

    area = area + sum_steps
    area = np.ceil((area / 2) - 1e-3) + 1

    return int(area)


def part_a(lines: List[str]) -> int:
    _input = parse(lines)

    # orientation of curve: https://en.wikipedia.org/wiki/Curve_orientation
    # if is_clockwise --> interior always to the right

    return compute_polygon_area(_input)


def part_b(lines: List[str]) -> int:
    _input = parse_b(lines)
    return compute_polygon_area(_input)


def run() -> None:
    print("partA:")
    assert part_a(read_input_to_list(__file__)) == 33491
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 62

    print("partB:")
    assert part_b(read_input_to_list(__file__)) == 87716969654406
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 952408144115
    print("done")
