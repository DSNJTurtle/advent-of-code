from typing import List, Tuple

import numpy as np
from aoc_2022.commons.commons import read_input_to_list


def parse(lines: List[str]):
    inst = []
    for l in lines:
        inst.append([s.strip() for s in l.split()])

    for e in inst:
        if len(e) == 2:
            e[1] = int(e[1])

    return inst


def apply(inst):
    cycles = [1]
    # print("start")
    for i in range(len(inst)):
        e = inst[i]
        # print(e)
        c = 1 if i == 0 else cycles[-1]
        if e[0] == "noop":
            cycles.append(c)
            # print(f"cycle={len(cycles)}: {cycles[-1]}")
        elif e[0] == "addx":
            cycles.extend([c, c + e[1]])
            # print(f"cycle={len(cycles) - 1}/{len(cycles)}: {str(cycles[-2:])}")
        else:
            raise RuntimeError("unknown instruction")

    return cycles


def part_a(lines: List[str]) -> int:
    # test
    test_lines = ["noop", "addx 3", "addx -5"]
    test_cycles = apply(parse(test_lines))
    # assert test_cycles == [1, 1, 4, 4, -1] # does not work without offset by 1
    assert test_cycles == [1, 1, 1, 4, 4, -1]
    # end test

    inst = parse(lines)
    cycles = apply(inst)

    signal = []
    for i in range(19, len(cycles), 40):
        signal.append(cycles[i] * (i + 1))

    sum = np.sum(signal)
    return sum


def part_b(lines: List[str]) -> int:
    pass


def run() -> None:
    print("partA:")
    assert part_a(read_input_to_list(__file__)) == 13680
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 13140

    print("partB:")
    # assert part_b(read_input_to_list(__file__)) == 2455
    # assert part_b(read_input_to_list(__file__, filename="test2.txt", read_test_input=True)) == 36

    print("done")
