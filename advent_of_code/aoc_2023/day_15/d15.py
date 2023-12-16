from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np

from advent_of_code.commons.commons import DoublyLinkedList, read_input_to_list


def compute_hash(input_str: str):
    x = 0
    for s in input_str:
        x += ord(s)
        x *= 17
        x = x % 256

    return x


def part_a(lines: List[str]) -> int:
    assert compute_hash("HASH") == 52
    parts = [s.strip() for s in lines[0].split(",")]
    hashes = [compute_hash(p) for p in parts]

    return np.sum(hashes)


@dataclass
class Data:
    label: str
    focal_length: int

    def __str__(self):
        return f"[{self.label},{self.focal_length}]"


@dataclass
class FocalPowers:
    box_nr: int
    powers: List[int]


def filter_by(d1: Data, d2: Data) -> bool:
    return d1.label == d2.label


def reduce_by(focal_powers: FocalPowers, data: Data):
    n = focal_powers.box_nr + 1
    slot = len(focal_powers.powers) + 1
    p = n * slot * data.focal_length
    focal_powers.powers.append(p)
    return focal_powers


def print_non_empty_boxes(boxes: List[DoublyLinkedList]):
    for i in range(len(boxes)):
        if boxes[i].size:
            print(f"box[{i}]: {str(boxes[i])}")


def part_b(lines: List[str]) -> int:
    parts = [s.strip() for s in lines[0].split(",")]
    boxes: List[DoublyLinkedList] = [DoublyLinkedList() for _ in range(256)]

    for p in parts:
        _p = p.split("=")
        op = "a" if len(_p) == 2 else "r"
        att = Data(label=_p[0].replace("-", ""), focal_length=None if op == "r" else int(_p[1]))
        box_nr = compute_hash(att.label)
        _list = boxes[box_nr]

        if op == "r":
            _list.remove(att, filter_by)
        else:
            # add or replace element
            if _node := _list.search(att, filter_by):
                _node.data = att  # replace
            else:
                _list.append(att)

    # compute focusing powers
    powers = []
    for i in range(len(boxes)):
        b = boxes[i]
        if b.size:
            r = b.reduce_left(reduce_by, initial=FocalPowers(i, list()))
            powers.extend(r.powers)

    return np.sum(powers)


def run() -> None:
    print("partA:")
    assert part_a(read_input_to_list(__file__)) == 510801
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 1320

    print("partB:")
    assert part_b(read_input_to_list(__file__)) == 212763
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 145

    print("done")
