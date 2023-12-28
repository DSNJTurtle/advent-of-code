from __future__ import annotations

from functools import cache
from typing import List

from advent_of_code.commons.commons import read_input_to_list


def parse_data(lines: List[str]):
    result = []
    for line in lines:
        row, nums = line.split()
        nums = tuple(int(num) for num in nums.split(","))
        result.append((row, nums))
    return result


@cache
def springs_finder(row, nums):
    next_part = nums[1:]
    springs = (f"{spr * '.'}{'#' * nums[0]}." for spr in range(len(row) - sum(nums) - len(next_part)))
    valid = (len(spr) for spr in springs if all(r in (c, "?") for r, c in zip(row, spr)))
    return (
        sum(springs_finder(row[v:], next_part) for v in valid)
        if next_part
        else sum("#" not in row[v:] for v in valid)
    )


def part_a(lines: List[str]):
    data = parse_data(lines)
    finder = [springs_finder(r + ".", n) for r, n in data]
    return sum(finder)


def part_b(lines: List[str]) -> int:
    data = parse_data(lines)
    new_springs = []
    for s in data:
        new_springs.append((((s[0] + "?") * 5)[:-1], s[1] * 5))
    finder = [springs_finder(r + ".", n) for r, n in new_springs]
    return sum(finder)


def run() -> None:
    print("partA:")
    res = part_a(read_input_to_list(__file__))
    print(res)
    assert res == 7407
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 21

    print("partB:")
    print(part_b(read_input_to_list(__file__)))
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 525152

    print("done")
