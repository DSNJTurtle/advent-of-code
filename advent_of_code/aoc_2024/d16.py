import heapq
import sys
from collections import defaultdict
from dataclasses import dataclass, field

from advent_of_code.commons.commons import read_input_to_list


@dataclass(frozen=True, order=True)
class Path:
    """Path class."""

    score: int
    pos: complex = field(compare=False)
    orientation: complex = field(compare=False)
    visited: set[complex] = field(compare=False)


def solve(lines: list[str]) -> tuple[int, int]:
    grid = {x + y * 1j: c for x, line in enumerate(lines) for y, c in enumerate(line)}
    pos = 0j
    end_pos = 0j
    for k, v in grid.items():
        if v == "S":
            pos = k
        if v == "E":
            end_pos = k

    dist = defaultdict(lambda: sys.maxsize)
    best_score = sys.maxsize
    best_tiles = set()
    paths = [Path(0, pos, 1j, {pos})]
    update = list(zip([1, 1j, -1j], [1, 1001, 1001], strict=False))
    while paths:
        p: Path = heapq.heappop(paths)

        if p.score > dist[p.pos, p.orientation]:
            continue
        else:
            dist[p.pos, p.orientation] = p.score

        if p.pos == end_pos and p.score <= best_score:
            best_score = p.score
            best_tiles = best_tiles | p.visited
            continue

        for o, c in update:
            new_orientation = p.orientation * o
            new_pos = p.pos + new_orientation
            if grid[new_pos] == "#":
                continue
            new_path = Path(p.score + c, new_pos, new_orientation, p.visited | {new_pos})
            heapq.heappush(paths, new_path)

    return best_score, len(best_tiles)


def part_a(lines: list[str]) -> int:
    x, _ = solve(lines)
    return x


def part_b(lines: list[str]) -> int:
    _, x = solve(lines)
    return x


def run() -> None:
    print("partA:")
    res = part_a(read_input_to_list(__file__))
    print(res)
    assert res == 109496
    # assert part_a(read_input_to_list(__file__, read_test_input=True)) == 7036  # first example
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 11048  # second example

    print("partB:")
    res = part_b(read_input_to_list(__file__))
    print(res)
    assert res == 551
    # assert part_b(read_input_to_list(__file__, read_test_input=True)) == 45  # first example
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 64  # second example

    print("done")
