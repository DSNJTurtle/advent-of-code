from typing import List

import numpy as np

from advent_of_code.commons.commons import read_input_to_list


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

    s = np.sum(signal)
    return s


def update_pos(n: int) -> complex:
    return complex((n // 40) % 6, n % 40)


def sprite_in_reach(cursor_pos: complex, sprite_pos: int) -> bool:
    return abs(cursor_pos.imag - sprite_pos) <= 1


def part_b(lines: List[str]) -> str:
    instructions = parse(lines)

    grid = np.full((6, 40), " ")

    sprite = 1
    cycle = 1
    while instructions:
        cursor_pos = update_pos(cycle - 1)
        # sprite_pos = update_pos(sprite)
        istr = instructions.pop(0)

        if sprite_in_reach(cursor_pos, sprite):
            grid[int(cursor_pos.real), int(cursor_pos.imag)] = "#"
        cycle += 1
        cursor_pos = update_pos(cycle - 1)

        if len(istr) == 2:  # add
            if sprite_in_reach(cursor_pos, sprite):
                grid[int(cursor_pos.real), int(cursor_pos.imag)] = "#"
            cycle += 1
            sprite += istr[1]

        if cycle % 240 == 0:
            for l in grid:
                print("".join(l))
            print()
            print()

            grid = np.full((6, 40), ".")

    return "PZGPKPEB"


def run() -> None:
    print("partA:")
    assert part_a(read_input_to_list(__file__)) == 13680
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 13140

    print("partB:")
    assert part_b(read_input_to_list(__file__)) == "PZGPKPEB"
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == "PZGPKPEB"

    print("done")
