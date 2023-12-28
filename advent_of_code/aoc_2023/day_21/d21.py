"""No clean code today"""
from __future__ import annotations

from typing import List

from advent_of_code.commons.commons import read_input_to_list


def parse_grid(lines: List[str]):
    grid = {complex(i, j): c.replace("S", "0") for i, r in enumerate(lines) for j, c in enumerate(r)}
    return grid


def part_a(lines: List[str], n_moves: int) -> int:
    grid = parse_grid(lines)

    starting_pos = [c for c in grid if grid[c] == "0"]
    end_pos = set()
    for moves in range(n_moves):
        for c in grid:
            if grid[c] == "0":
                grid[c] = "."

        while starting_pos:
            pos = starting_pos.pop()
            for m in [1, -1, 1j, -1j]:
                new_pos = pos + m
                if (v := grid.get(new_pos)) and v != "#":
                    end_pos.add(new_pos)

        starting_pos = end_pos
        end_pos = set()

    return len(starting_pos)


def grid_coord(x: complex, n_rows: int, n_cols: int):
    r = -(abs(x.real) // n_rows) - 1 if x.real < -0.5 else x.real // n_rows
    i = -(abs(x.imag) // n_cols) - 1 if x.imag < -0.5 else x.imag // n_cols
    return complex(r, i)


def part_b(lines: List[str], n_moves: int) -> int:
    assert grid_coord(complex(0, 1), 2, 2) == complex(0, 0)
    assert grid_coord(complex(1, 1), 2, 2) == complex(0, 0)
    assert grid_coord(complex(2, 1), 2, 2) == complex(1, 0)
    assert grid_coord(complex(1, 2), 2, 2) == complex(0, 1)
    assert grid_coord(complex(2, 2), 2, 2) == complex(1, 1)
    assert grid_coord(complex(-0, 1), 2, 2) == complex(0, 0)
    assert grid_coord(complex(-1, 1), 2, 2) == complex(-1, 0)
    assert grid_coord(complex(-0, -0), 2, 2) == complex(0, 0)

    grid = parse_grid(lines)
    n_rows = int(max([c.real for c in grid])) + 1
    n_cols = int(max([c.imag for c in grid])) + 1

    starting_pos = [c for c in grid if grid[c] == "0"]
    for c in grid:
        if grid[c] == "0":
            grid[c] = "."

    end_pos = set()
    n_move = 0
    while True:
        n_move += 1
        while starting_pos:
            pos = starting_pos.pop()
            for m in [1, -1, 1j, -1j]:
                new_pos = pos + m
                new_map_pos = complex(new_pos.real % n_rows, new_pos.imag % n_cols)
                if (v := grid.get(new_map_pos)) and v != "#":
                    end_pos.add(new_pos)

        starting_pos = end_pos
        end_pos = set()

        if (n_move - 65) % 131 == 0:
            print(f"n_moves = {n_move}: {len(starting_pos)} tiles")
        if n_move > 1000:
            break

    return len(starting_pos)


def run() -> None:
    print("partA:")
    print(part_a(read_input_to_list(__file__), n_moves=64))
    assert part_a(read_input_to_list(__file__), n_moves=64) == 3562
    assert part_a(read_input_to_list(__file__, read_test_input=True), n_moves=6) == 16

    print("partB:")
    x = (26501365 - 65) / 131
    a = int(14483 * x**2 + 14603 * x + 3682)  # quadratic fit
    assert a == 592723929260582
    print(part_b(read_input_to_list(__file__), n_moves=26501365))
    print("done")
