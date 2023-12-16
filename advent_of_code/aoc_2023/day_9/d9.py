from typing import List

import numpy as np

from advent_of_code.commons.commons import read_input_to_list


def parse(lines: List[str]):
    readings = []
    for l in lines:
        readings.append(np.array([int(s) for s in l.strip().split()], dtype=int))

    return readings


def next_element_for_reading(reading: np.ndarray) -> int:
    pyramid = [reading]
    curr_a = pyramid[-1]
    while np.any(curr_a):
        next_a = np.roll(curr_a, -1)
        diff = (next_a - curr_a)[:-1]
        pyramid.append(diff)
        curr_a = diff

    val_to_add = 0
    pyramid.reverse()
    for e in pyramid:
        val_to_add += e[-1]

    return val_to_add


def prev_element_for_reading(reading: np.ndarray) -> int:
    pyramid = [np.flip(reading)]
    curr_a = pyramid[-1]
    while np.any(curr_a):
        next_a = np.roll(curr_a, 1)
        diff = (next_a - curr_a)[1:]
        pyramid.append(diff)
        curr_a = diff

    val_to_add = 0
    pyramid.reverse()
    for e in pyramid:
        val_to_add = e[-1] - val_to_add

    return val_to_add


def part_a(lines: List[str]) -> int:
    readings = parse(lines)
    next_elements = [next_element_for_reading(r) for r in readings]

    return np.sum(next_elements)


def part_b(lines: List[str]) -> int:
    readings = parse(lines)
    prev_elements = [prev_element_for_reading(r) for r in readings]

    return np.sum(prev_elements)


def run() -> None:
    print("partA:")
    assert part_a(read_input_to_list(__file__)) == 1834108701
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 114

    print("partB:")
    assert part_b(read_input_to_list(__file__)) == 993
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 2

    print("done")
