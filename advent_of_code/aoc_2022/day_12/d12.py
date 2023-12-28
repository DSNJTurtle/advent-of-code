import heapq
import string
from dataclasses import dataclass, field
from typing import List

from advent_of_code.commons.commons import read_input_to_list


def parse_grid(lines: List[str]):
    conv = {c: i + 1 for i, c in enumerate(string.ascii_lowercase)}
    grid = {complex(i, j): conv.get(c, c) for i, r in enumerate(lines) for j, c in enumerate(r)}

    s, e = 0j, 0j
    for p, c in grid.items():
        if c == "S":
            s = p
            grid[p] = conv["a"]
        if c == "E":
            e = p
            grid[p] = conv["z"]

    return s, e, grid


@dataclass(frozen=True, order=True)
class Cell:
    n_steps: int
    char: int
    pos: complex = field(compare=False)


def dijkstra(grid, start, end):
    open_positions = [Cell(0, grid[start], start)]
    visited = set()

    while open_positions:
        c = heapq.heappop(open_positions)
        if c.pos in visited:
            continue
        visited.add(c.pos)

        if c.pos == end:
            return c.n_steps

        for step in [1, -1, 1j, -1j]:
            new_pos = c.pos + step
            if (new_char := grid.get(new_pos)) and new_char - c.char <= 1:
                heapq.heappush(open_positions, Cell(c.n_steps + 1, new_char, new_pos))

    return -1


def part_a(lines: List[str]) -> int:
    s, e, grid = parse_grid(lines)
    n_steps = dijkstra(grid, s, e)
    return n_steps


def part_b(lines: List[str]) -> int:
    s, e, grid = parse_grid(lines)
    starting_positions = [pos for pos in grid if grid[pos] == 1]
    n_steps = [dijkstra(grid, s, e) for s in starting_positions]
    min_steps = min([n for n in n_steps if n > 0])
    return min_steps


def run() -> None:
    print("partA:")
    print(part_a(read_input_to_list(__file__)))
    assert part_a(read_input_to_list(__file__)) == 394
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 31

    print("partB:")
    print(part_b(read_input_to_list(__file__)))
    assert part_b(read_input_to_list(__file__)) == 388
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 29

    print("done")
