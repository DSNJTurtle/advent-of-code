from typing import List

from advent_of_code.commons.commons import read_input_to_list


def get_pairs(lines: List[str]):
    pairs = []
    for l in lines:
        parts = l.split(",")
        p = []
        for part in parts:
            p.append([int(i.strip()) for i in part.split("-")])

        pairs.append(p)

    return pairs


def is_pair_in_range(pair, range):
    if range[0] <= pair[0] and pair[1] <= range[1]:
        return True

    return False


def has_overlap(p1, p2):
    if p2[0] <= p1[0] <= p2[1] or p2[0] <= p1[1] <= p2[1]:
        return True

    return False


def part_a(lines: List[str]) -> int:
    pairs = get_pairs(lines)

    res = 0
    for p in pairs:
        e1 = p[0]
        e2 = p[1]
        if is_pair_in_range(e1, e2) or is_pair_in_range(e2, e1):
            res += 1

    return res


def part_b(lines: List[str]) -> int:
    pairs = get_pairs(lines)

    res = 0
    for p in pairs:
        if has_overlap(p[0], p[1]) or has_overlap(p[1], p[0]):
            res += 1

    return res


def run() -> None:
    print("partA:")
    assert part_a(read_input_to_list(__file__)) == 441
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 2

    print("partB:")
    assert part_b(read_input_to_list(__file__)) == 861
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 4

    print("done")
