from typing import List

import numpy as np

from advent_of_code.commons.commons import read_input_to_list


def get_calories(lines: List[str]):
    calories = []
    elf = []
    for l in lines:
        _l = l.strip()
        if _l == "":
            calories.append(np.sum(elf))
            elf = []

        else:
            elf.append(int(_l))

    # last line
    calories.append(np.sum(elf))

    return calories


def part_a(lines: List[str]) -> int:
    calories = get_calories(lines)
    return np.max(calories)


def part_b(lines: List[str]) -> int:
    calories = get_calories(lines)
    calories = sorted(calories, reverse=True)
    calories = calories[:3]

    return np.sum(calories)


def run() -> None:
    print("partA:")
    assert part_a(read_input_to_list(__file__)) == 70613
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 24000

    print("partB:")
    assert part_b(read_input_to_list(__file__)) == 205805
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 45000

    print("done")
