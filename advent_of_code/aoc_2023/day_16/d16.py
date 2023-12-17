"""Replace caching solution with complex numbers. Inspiration taken from https://topaz.github.io/paste/#XQAAAQAUAwAAAAAAAAAziAOiE/kI+atcxglPNa1Z5ByKIiDHt58MHifgG2R3rf+zqKYQZv1B457oZ4kCsEABs+9eoKiNQRgfhGTI51bj3uRshO3PWkcO2ujzAaCpLjowdp1GKNTOnkukUGRQKdOcsHDROmva3wF9HKvBRmDVX57YyOReLWiXWu7VZ6BH+4I4+HYwrpO4f3Cnm0z1SibCaOiKz4eojGMOAGzZZpSzQOL3fz30dX5Pyz12ucW45Yuu+ZiaJ7UdH/MYB9mWGHziy8uujcM+VxQUCWPjkRQ0XdsUM3PC+CTKPYXP2Gyaq+wyME55uuGsNGBw46QrFtVC+Shv2NuT8LF2oxefM5bcWLHsbpmwLCIV0EqhAiT5KgU7RRDjVOGA4hLybRH7NlZSaFrNUASfRa+QEb2StcGlaaQnm5IpLIJ0ngBwFVo1XbqqDcxOKAMUfyPEs1EQR2JOm/9/+sQBjXgiCNWpr//6SPk0"""
from __future__ import annotations

from typing import List

import numpy as np
from tqdm import tqdm

from advent_of_code.commons.commons import read_input_to_list


def parse_grid(lines: List[str]):
    return {complex(i, j): c for i, r in enumerate(lines) for j, c in enumerate(r)}


def energised_tiles_from_starting_position(grid, start_pos, start_d):
    # pgrid = PrintGrid(grid)
    # right/left = 1j/-1j, up/down = -1/+1
    todo = [(start_pos, start_d)]
    done = set()
    while todo:
        pos, d = todo.pop()
        while not (pos, d) in done:
            done.add((pos, d))
            pos += d
            # pgrid.update([pos])
            match grid.get(pos):
                case "|":
                    d = -1
                    todo.append((pos, -d))
                case "-":
                    d = 1j
                    todo.append((pos, -d))
                case "/":
                    d = (d * 1j).conjugate()  # -complex(im,re)
                case "\\":
                    d = -(d * 1j).conjugate()  # complex(im,re)
                case None:
                    break  # reached end

            # pgrid.show()

    pos = list({pos for pos, _ in done})

    return len(pos) - 1  # remove start


class PrintGrid:
    def __init__(self, grid, initial="."):
        self.initial = initial
        n_rows = int(max(k.real for k in grid)) + 1
        n_cols = int(max(k.imag for k in grid)) + 1
        self.grid = np.zeros((n_rows, n_cols), dtype=int)

    def show(self):
        print()
        for g in self.grid:
            print(" ".join([str(i) for i in g]).replace("0", self.initial))

        print()
        print()

    def update(self, entries: List[complex]) -> None:
        for e in entries:
            re, im = e.real, e.imag
            if 0 <= re < len(self.grid) and 0 <= im < len(self.grid[0]):
                self.grid[int(e.real)][int(e.imag)] += 1


def part_a(lines: List[str]) -> int:
    grid = parse_grid(lines)
    return energised_tiles_from_starting_position(grid, -1j, 1j)


def part_b(lines: List[str]) -> int:
    grid = parse_grid(lines)

    starting_positions = []
    # from left and right
    for i in range(len(lines)):
        starting_positions.append((complex(i, -1), 1j))
        starting_positions.append((complex(i, len(lines[0])), -1j))
    # from top and bottom
    for j in range(len(lines[0])):
        starting_positions.append((complex(-1, j), 1))
        starting_positions.append((complex(len(lines), j), -1))

    tiles = []
    for sc, md in tqdm(starting_positions):
        tiles.append(energised_tiles_from_starting_position(grid, sc, md))

    return np.max(tiles)


def run() -> None:
    print("partA:")
    assert part_a(read_input_to_list(__file__)) == 7608
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 46

    print("partB:")
    assert part_b(read_input_to_list(__file__)) == 8221
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 51

    print("done")
