from __future__ import annotations

import heapq
from typing import Dict, List

from advent_of_code.commons.commons import read_input_to_list


def parse_dict(lines: List[str]):
    return {complex(i, j): int(c) for i, r in enumerate(lines) for j, c in enumerate(r)}


def dijkstra(grid: Dict, min_steps: int, max_steps: int):
    # directions: right/left = +-1j, down/up = +-1
    # entries in queue: (heat_loss, tie_breaker, position, direction, steps)
    # tie breaker needed because complex numbers are not comparable
    # ignore starting cell because it is not counted
    q = [(grid[1 + 0j], 0, 1 + 0j, 1, 1), (grid[1j], 1, 1j, 1j, 1)]
    heapq.heapify(q)

    tb = 2
    visited = set()
    end = complex(max([x.real for x in grid]), max([x.imag for x in grid]))
    while q:
        heat_loss, _, pos, d, s = heapq.heappop(q)
        if pos == end and s >= min_steps:
            return heat_loss
        if (pos, d, s) in visited:
            continue
        visited.add((pos, d, s))
        if s < (max_steps - 1) and (h := grid.get(pos + d)):
            # new forward step, if allowed
            tb += 1
            heapq.heappush(q, (heat_loss + h, tb, pos + d, d, s + 1))
        if s >= min_steps:
            # add left/right neighbors
            new_directions = [d * 1j, -d * 1j]
            for new_d in new_directions:
                new_pos = pos + new_d
                if h := grid.get(new_pos):
                    tb += 1
                    heapq.heappush(q, (heat_loss + h, tb, new_pos, new_d, 0))


def part_a(lines: List[str]) -> int:
    grid = parse_dict(lines)
    heat_loss = dijkstra(grid, 0, 3)

    return heat_loss


def part_b(lines: List[str]) -> int:
    grid = parse_dict(lines)
    heat_loss = dijkstra(grid, 3, 10)

    return heat_loss


def run() -> None:
    print("partA:")
    assert part_a(read_input_to_list(__file__)) == 797
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 102

    print("partB:")
    assert part_b(read_input_to_list(__file__)) == 914
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 94
    assert part_b(read_input_to_list(__file__, filename="test2.txt", read_test_input=True)) == 71

    print("done")
