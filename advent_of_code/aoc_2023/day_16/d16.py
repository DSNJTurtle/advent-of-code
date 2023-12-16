from __future__ import annotations

from functools import cache
from typing import List, Tuple

import numpy as np
from tqdm import tqdm

from advent_of_code.commons.commons import read_input_to_list

MOVING_DIRECTION_SPLITS = {
    "R": {"/": ["U"], "\\": ["D"], "|": ["U", "D"]},
    "L": {"/": ["D"], "\\": ["U"], "|": ["U", "D"]},
    "U": {"/": ["R"], "\\": ["L"], "-": ["L", "R"]},
    "D": {"/": ["L"], "\\": ["R"], "-": ["L", "R"]},
}


def inner_single_move(
    grid: np.ndarray, start_cell: Tuple[int, int], direction: str
) -> Tuple[Tuple[int, int], List[Tuple[int, int]]]:
    m, n = start_cell
    energized_cells = [start_cell]
    if direction == "R":
        jj = n + 1
        for jj in range(n + 1, len(grid[m])):
            if grid[m, jj] in MOVING_DIRECTION_SPLITS[direction]:
                break
            energized_cells.append((m, jj))

        return (m, jj), energized_cells

    elif direction == "L":
        jj = n - 1
        for jj in range(n - 1, -1, -1):
            if grid[m, jj] in MOVING_DIRECTION_SPLITS[direction]:
                break
            energized_cells.append((m, jj))

        return (m, jj), energized_cells

    elif direction == "U":
        ii = m - 1
        for ii in range(m - 1, -1, -1):
            if grid[ii, n] in MOVING_DIRECTION_SPLITS[direction]:
                break
            energized_cells.append((ii, n))

        return (ii, n), energized_cells

    elif direction == "D":
        ii = m + 1
        for ii in range(m + 1, len(grid[:, n])):
            if grid[ii, n] in MOVING_DIRECTION_SPLITS[direction]:
                break
            energized_cells.append((ii, n))

        return (ii, n), energized_cells

    else:
        raise RuntimeError("invalid direction")


def parse_grid(lines: List[str]):
    grid = []
    for l in lines:
        grid.append([str(s) for s in l])

    return np.array(grid)


def energised_tiles_from_starting_position(grid, starting_cell, starting_move, move_func):
    n_rows = len(grid)
    n_cols = len(grid[0])

    next_moves = [(starting_cell, starting_move)]
    already_visited = set(next_moves)
    energised_cells = list()

    while next_moves:
        s_cell, moving_direction = next_moves.pop()
        already_visited.add((s_cell, moving_direction))
        next_cell, ec = move_func(s_cell, moving_direction)
        i, j = next_cell
        if 0 <= i < n_rows and 0 <= j < n_cols:
            # otherwise reached end
            for next_moving_dir in MOVING_DIRECTION_SPLITS[moving_direction].get(
                grid[i, j], moving_direction
            ):
                nm = (next_cell, next_moving_dir)
                if nm not in already_visited:
                    next_moves.append(nm)

        energised_cells.extend(ec)
        energised_cells = list(set(energised_cells))

    return len(energised_cells) - 1  # remove  start cell


def part_a(lines: List[str]) -> int:
    grid = parse_grid(lines)

    @cache
    def move(start_cell: Tuple[int, int], direction: str) -> Tuple[Tuple[int, int], List[Tuple[int, int]]]:
        return inner_single_move(grid, start_cell, direction)

    return energised_tiles_from_starting_position(grid, (0, -1), "R", move)


def part_b(lines: List[str]) -> int:
    grid = parse_grid(lines)

    @cache
    def move(start_cell: Tuple[int, int], direction: str) -> Tuple[Tuple[int, int], List[Tuple[int, int]]]:
        return inner_single_move(grid, start_cell, direction)

    starting_positions = []
    # from left and right
    for i in range(len(grid)):
        starting_positions.append(((i, -1), "R"))
        starting_positions.append(((i, len(grid[0])), "L"))
    # from top and bottom
    for j in range(len(grid[0])):
        starting_positions.append(((-1, j), "D"))
        starting_positions.append(((len(grid), j), "U"))

    tiles = []
    for sc, md in tqdm(starting_positions):
        tiles.append(energised_tiles_from_starting_position(grid, sc, md, move))

    return np.max(tiles)


def run() -> None:
    print("partA:")
    assert part_a(read_input_to_list(__file__)) == 7608
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 46

    print("partB:")
    assert part_b(read_input_to_list(__file__)) == 8221
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 51

    print("done")
