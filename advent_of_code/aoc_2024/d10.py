import copy
from dataclasses import dataclass, replace

from advent_of_code.commons.commons import read_input_to_list


def parse(lines: list[str]):
    grid = {complex(i, j): int(s) for i, line in enumerate(lines) for j, s in enumerate(line)}

    start_pos = [key for key, value in grid.items() if value == 0]

    return grid, start_pos


@dataclass
class Trail:
    """Trail."""

    head: complex
    pos: complex
    visited: list[complex]


def solve(lines: list[str], is_part_b: bool):
    grid, start_positions = parse(lines)

    open_trails = [Trail(head=x, pos=x, visited=[x]) for x in start_positions]
    closed_trails = []

    while len(open_trails) > 0:
        t = open_trails.pop(0)
        if grid.get(t.pos) == 9:
            closed_trails.append(t)
            continue

        for update in [complex(0, 1), complex(0, -1), complex(1, 0), complex(-1, 0)]:
            new_pos = t.pos + update
            if grid.get(new_pos) is not None:
                if new_pos in t.visited:
                    continue
                current_c = grid[t.pos]
                new_c = grid[new_pos]
                if new_c - current_c != 1:
                    continue

                new_t = replace(t, pos=new_pos, visited=copy.deepcopy(t.visited))
                new_t.visited.append(new_pos)
                open_trails.append(new_t)

    if is_part_b:
        res = len(closed_trails)
    else:
        # drop duplicates
        reduced_closed_trails = {(t.head, t.visited[-1]): t for t in closed_trails}
        res = len(reduced_closed_trails)

    return res


def part_a(lines: list[str]) -> int:
    return solve(lines, False)


def part_b(lines: list[str]) -> int:
    return solve(lines, True)


def run() -> None:
    print("partA:")
    res = part_a(read_input_to_list(__file__))
    print(res)
    assert res == 667
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 36

    print("partB:")
    res = part_b(read_input_to_list(__file__))
    print(res)
    assert res == 1344
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 81

    print("done")
