import string
from typing import List

import numpy as np
from aoc_2022.commons.commons import read_input_to_list


def compartments_per_rucksack(s: str) -> List[str]:
    l = len(s)
    assert l % 2 == 0
    c1 = s[: l // 2]
    c2 = s[l // 2 :]

    return [c1, c2]


def char_prio():
    chars = string.ascii_lowercase + string.ascii_uppercase
    prios = {}
    for i, c in enumerate(chars):
        prios[c] = i + 1

    return prios


def part_a(lines: List[str]) -> int:
    rucksacks = [compartments_per_rucksack(l.strip()) for l in lines]
    items = []
    for r in rucksacks:
        r1 = set(r[0])
        r2 = set(r[1])
        for s in r1:
            if s in r2:
                items.append(s)

    prio = char_prio()
    scores = [prio[c] for c in items]

    return np.sum(scores)


def find_element_per_group(g) -> str:
    d = {}
    for e in g:
        for s in set(e):
            d[s] = d.get(s, 0) + 1

    for k in d:
        if d[k] == 3:
            return k


def part_b(lines: List[str]) -> int:
    groups = [lines[n : n + 3] for n in range(0, len(lines), 3)]
    items = [find_element_per_group(g) for g in groups]
    prio = char_prio()
    scores = [prio[c] for c in items]

    return np.sum(scores)


def run() -> None:
    print("partA:")
    assert part_a(read_input_to_list(__file__)) == 8349
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 157

    print("partB:")
    assert part_b(read_input_to_list(__file__)) == 2681
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 70

    print("done")
