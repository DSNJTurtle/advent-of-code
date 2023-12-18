from __future__ import annotations

from typing import List

import numpy as np

from advent_of_code.commons.commons import read_input_to_list


def parse(lines: List[str]):
    grid = {complex(i, j): str(s) for i, l in enumerate(lines) for j, s in enumerate(l)}

    return grid


def parse_b(lines: List[str]):
    grid = [list(l.strip()) for l in lines]
    return np.array(grid)


def move_grid(grid):
    n_rows = len(grid)
    n_cols = len(grid[0])

    for c in range(n_cols):
        for r in range(n_rows):
            tmp_r = r
            if grid[tmp_r, c] == "O":
                while True:
                    i = tmp_r - 1
                    if i >= 0 and grid[i, c] == ".":
                        grid[i, c] = "O"
                        grid[tmp_r, c] = "."
                        tmp_r = i
                    else:
                        break
            else:
                continue


def count_load(grid):
    n_rows = len(grid)
    n_cols = len(grid[0])
    s = 0
    for r in range(n_rows):
        count = 0
        for c in range(n_cols):
            if grid[r][c] == "O":
                count += 1
        s += count * (n_rows - r)

    return s


def part_a(lines: List[str]) -> int:
    grid = parse_b(lines)

    move_grid(grid)
    load = count_load(grid)
    return load


def part_b(lines: List[str]) -> int:
    grid = parse_b(lines)
    target_cycles = 1_000_000_000

    cycles = 0
    states = {}
    while True:
        if cycles % 100_000 == 0:
            print(f"cycles: {cycles}")
        if states is not None:
            new_state = tuple(
                [(i, j) for i in range(len(grid)) for j in range(len(grid[0])) if grid[i, j] == "O"]
            )
            if new_state in states:
                cycles = target_cycles - (target_cycles - cycles) % (cycles - states[new_state])
                states = None  # stop tracking when we found a period
            else:
                states[new_state] = cycles

        move_grid(grid)
        grid = np.rot90(grid, k=-1)
        move_grid(grid)
        grid = np.rot90(grid, k=-1)
        move_grid(grid)
        grid = np.rot90(grid, k=-1)
        move_grid(grid)
        grid = np.rot90(grid, k=-1)

        cycles += 1
        if cycles >= target_cycles:
            break

    load = count_load(grid)
    return load


def run() -> None:
    print("partA:")
    assert part_a(read_input_to_list(__file__)) == 103614
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 136

    print("partB:")
    assert part_b(read_input_to_list(__file__)) == 83790
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 64

    print("done")
