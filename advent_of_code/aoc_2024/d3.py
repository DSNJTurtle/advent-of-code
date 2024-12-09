import re

import numpy as np

from advent_of_code.commons.commons import read_input_to_list


def part_a(lines: list[str]) -> int:
    p = re.compile(r"mul\([0-9]{1,3},[0-9]{1,3}\)")
    line = "".join(lines)
    g = p.findall(line)
    g = [str(x).replace("mul(", "").replace(")", "").replace(",", "*") for x in g]
    s = np.sum([eval(x) for x in g])

    return s


def part_b(lines: list[str]) -> int:
    p = re.compile(r"mul\([0-9]{1,3},[0-9]{1,3}\)|do\(\)|don't\(\)")
    line = "".join(lines)

    s = 0
    include = True
    multiplications = []

    for m in p.findall(line):
        if str(m).startswith("mul") and include:
            multiplications.append(str(m))
        elif str(m) == "do()":
            include = True
        elif str(m) == "don't()":
            include = False
        else:
            continue

    g = [str(x).replace("mul(", "").replace(")", "").replace(",", "*") for x in multiplications]
    s += np.sum([eval(x) for x in g])

    return s


def run() -> None:
    print("partA:")
    res = part_a(read_input_to_list(__file__))
    print(res)
    assert res == 179571322
    # assert part_a(read_input_to_list(__file__, read_test_input=True)) == 161

    print("partB:")
    res = part_b(read_input_to_list(__file__))
    print(res)
    assert res == 103811193
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 48

    print("done")
