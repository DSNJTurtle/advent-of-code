from __future__ import annotations

import os
from functools import cache
from pathlib import Path
from typing import List

import numpy as np
from tqdm import tqdm

from advent_of_code.commons.commons import read_input_to_list


class Node:
    def __init__(self, completed_str: str, remaining_str: str, target: List[int], parent: Node | None = None):
        self.parent = parent
        # if self.parent is None:
        #     print(f"{remaining_str}  {target}")
        self.target = target
        self.left = None
        self.right = None

        next_question_mark_pos = remaining_str.find("?")
        if next_question_mark_pos != -1:
            # offset string to next question mark
            self.completed_str = completed_str + remaining_str[:next_question_mark_pos]
            self.remaining_str = remaining_str[next_question_mark_pos:]
        else:
            self.completed_str = completed_str + remaining_str
            self.remaining_str = ""

        # current node still valid?
        self.is_still_valid = self.still_valid_config()
        self.is_valid_leaf = self.is_still_valid and len(self.remaining_str) == 0
        # if self.is_valid_leaf:
        #     print(f"{self.completed_str}")

        # create children if needed
        if self.is_still_valid and len(self.remaining_str) > 0:
            self.left = self.create_child(next_char=".")
            self.right = self.create_child(next_char="#")

    def create_child(self, next_char: str):
        n = Node(self.completed_str + next_char, self.remaining_str[1:], self.target, self)
        cond = n.is_valid_leaf or (n.is_still_valid and (n.left is not None or n.right is not None))
        if not cond:
            n = None

        return n

    def extract_config(self) -> List[int]:
        config = []
        broken_counter = 0
        for s in self.completed_str:
            if s == "#":
                broken_counter += 1
            elif s == "." and broken_counter > 0:
                config.append(broken_counter)
                broken_counter = 0
            else:
                continue

        if broken_counter > 0:
            config.append(broken_counter)

        return config

    def still_valid_config(self) -> bool:
        config = self.extract_config()

        if len(self.remaining_str) == 0:
            # at the end everything must be correct
            return config == self.target

        if len(config) > len(self.target):
            return False

        # take first n-1 elements
        lc = max(len(config) - 1, 0)
        c = config[:lc]
        t = self.target[:lc]
        remaining_t = self.target[lc + 1 :]
        if np.sum(remaining_t) + len(remaining_t) - 1 > len(self.remaining_str):
            return False
        res = c == t
        return res

    def count_leafs(self) -> int:
        if self.is_valid_leaf:
            return 1

        n_leafs = 0
        n_leafs += self.left.count_leafs() if self.left else 0
        n_leafs += self.right.count_leafs() if self.right else 0

        return n_leafs


def parse(lines: List[str]):
    springs = []
    for l in lines:
        p = l.split()
        configs = [int(s.strip()) for s in p[1].split(",")]
        springs.append((p[0].strip(), configs))

    return springs


def parse2(lines: List[str]):
    springs = []
    for l in lines:
        p = l.split()
        configs = [int(s.strip()) for s in p[1].split(",")]
        spring_parts = [x for x in p[0].strip().split(".") if x != ""]
        springs.append((p[0].strip(), configs))

    return springs


def get_config(config_str):
    config = []
    broken_counter = 0
    for s in config_str:
        if s == "#":
            broken_counter += 1
        elif s == "." and broken_counter > 0:
            config.append(broken_counter)
            broken_counter = 0
        else:
            continue

    if broken_counter > 0:
        config.append(broken_counter)

    return config


def replace_question_marks(s: str, combination):
    _s = s
    for c in combination:
        _s = _s.replace("?", c, 1)

    return _s


def replace_question_marks_new(s: str):
    _s = [s]
    s_new = []
    for _ in range(s.count("?")):
        for x in _s:
            s_new.extend([x.replace("?", ".", 1), x.replace("?", "#", 1)])

        _s = s_new
        s_new = []

    return _s


def parse_data(my_file):
    with open(my_file) as f:
        result = []
        for line in f.readlines():
            row, nums = line.split()
            nums = tuple(int(num) for num in nums.split(","))
            result.append((row, nums))
        return result


def part_a(lines: List[str]) -> int:
    assert get_config("#.#.###") == [1, 1, 3]
    assert get_config(".#...#....###.") == [1, 1, 3]
    assert get_config(".#.###.#.######") == [1, 3, 1, 6]
    assert get_config("##.###.#.######") != [1, 3, 1, 6]

    springs = parse(lines)
    arragements = []
    for s in springs:
        n_arragements = 0
        comb = replace_question_marks_new(s[0])
        for c in comb:
            if get_config(c) == s[1]:
                n_arragements += 1

        arragements.append(n_arragements)

    return np.sum(arragements)


def part_a2(lines: List[str]) -> int:
    assert get_config("#.#.###") == [1, 1, 3]
    assert get_config(".#...#....###.") == [1, 1, 3]
    assert get_config(".#.###.#.######") == [1, 3, 1, 6]
    assert get_config("##.###.#.######") != [1, 3, 1, 6]

    springs = parse(lines)
    arrangements = []
    for s in tqdm(springs):
        n = Node("", s[0], s[1])
        arrangements.append(n.count_leafs())

    return np.sum(arrangements)


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


def part_a3(lines: List[str]):
    test = parse_data(os.path.join(Path(__file__).parent, "test.txt"))
    finder = [springs_finder(r + ".", n) for r, n in test]


def part_b(lines: List[str]) -> int:
    springs = parse(lines)
    new_springs = []
    for s in springs:
        new_springs.append([((s[0] + "?") * 5)[:-1], s[1] * 5])

    arrangements = []
    for s in tqdm(new_springs):
        n = Node("", s[0], s[1])
        arrangements.append(n.count_leafs())

    return np.sum(arrangements)


def run() -> None:
    print("partA:")
    # assert part_a2(read_input_to_list(__file__)) == 7407
    assert part_a3(read_input_to_list(__file__, read_test_input=True)) == 21

    print("partB:")
    # print(part_b(read_input_to_list(__file__)))
    # assert part_b(read_input_to_list(__file__, read_test_input=True)) == 525152

    print("done")
