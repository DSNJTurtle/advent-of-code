import re
from typing import List

import numpy as np

from advent_of_code.commons.commons import read_input_to_list


def part_a(lines: List[str]) -> int:
    n1 = [re.sub("\D", "", s) for s in lines]
    n2 = ["".join([s[0], s[-1]]) for s in n1]
    n3 = np.sum([int(s) for s in n2])
    return n3


def part_b(lines: List[str]) -> int:
    numbers = [
        ("one", "o1e"),
        ("two", "t2o"),
        ("three", "t3e"),
        ("four", "f4r"),
        ("five", "f5e"),
        ("six", "s6"),
        ("seven", "s7n"),
        ("eight", "e8t"),
        ("nine", "n9e"),
    ]
    result = []
    for l in lines:
        for ns, nn in numbers:
            l = l.replace(ns, nn)

        result.append(l)

    n1 = [re.sub("\D", "", s) for s in result]
    n2 = ["".join([s[0], s[-1]]) for s in n1]
    n3 = np.sum([int(s) for s in n2])
    return n3


def run() -> None:
    print("partA:")
    print(part_a(read_input_to_list(__file__)))
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 142

    print("partB:")
    print(part_b(read_input_to_list(__file__)))
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 281

    print("done")
