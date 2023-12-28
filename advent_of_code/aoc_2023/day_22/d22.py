from __future__ import annotations

from typing import List

from advent_of_code.commons.commons import read_input_to_list


def parse_snapshot(lines: List[str]):
    bricks = {}
    for i, l in enumerate(lines):
        ll = l.split("~")
        start_pos = tuple(int(x.strip()) for x in ll[0].split(","))
        end_pos = tuple(int(x.strip()) for x in ll[1].split(","))
        if start_pos[2] > end_pos[2]:
            _t = start_pos
            start_pos = end_pos
            end_pos = _t

        bricks[i] = (start_pos, end_pos)

    return bricks


def get_grid(bricks):
    max_x = max(max(b[0][0], b[1][0]) for i, b in bricks.items())
    max_y = max(max(b[0][1], b[1][1]) for i, b in bricks.items())
    grid = {(i, j): {0: -1} for i in range(max_x + 1) for j in range(max_y + 1)}
    assert all([is_vertical(bricks[b]) or is_horizontal(bricks[b]) for b in bricks])
    return grid


def is_vertical(brick):
    s, e = brick
    if s[:2] != e[:2]:
        return False
    return True


def is_horizontal(brick):
    s, e = brick
    if s[2] != e[2]:
        return False
    return True


def get_all_pos_for_horizontal_brick(brick):
    s, e = brick
    diff_x = e[0] - s[0]
    diff_y = e[1] - s[1]
    ax = abs(diff_x)
    ay = abs(diff_y)
    assert ax == 0 or ay == 0  # no diagonal movement
    length = max(ax, ay)
    ux = 1 if ax > 0 else 0
    uy = 1 if ay > 0 else 0
    all_xy_pos = [(s[0] + i * ux, s[1] + i * uy) for i in range(length + 1)]
    return all_xy_pos


def settle_bricks(grid, bricks):
    sorted_bricks = sorted(list(bricks.items()), key=lambda x: x[1][0][2])
    for i, b in sorted_bricks:
        s, e = b
        if is_horizontal(b):
            all_xy_pos = get_all_pos_for_horizontal_brick(b)
            next_free_z = max(z for x in all_xy_pos for z in grid[x]) + 1
            shift = s[2] - next_free_z
            new_s = (s[0], s[1], s[2] - shift)
            new_e = (e[0], e[1], e[2] - shift)
            bricks[i] = (new_s, new_e)
            for x in all_xy_pos:
                grid[x][new_e[2]] = i
        else:
            # vertical
            next_free_cell = max(z for z in grid[s[:2]]) + 1
            shift = s[2] - next_free_cell
            assert shift >= 0
            new_s = (s[0], s[1], s[2] - shift)
            new_e = (e[0], e[1], e[2] - shift)
            bricks[i] = (new_s, new_e)
            grid[s[:2]][new_e[2]] = i
            grid[s[:2]][new_s[2]] = i


def get_supports(grid, bricks):
    sorted_bricks = sorted(list(bricks.items()), key=lambda x: x[1][0][2])
    supports = {i: set() for i, _ in sorted_bricks}
    for i, b in sorted_bricks:
        s, e = b
        if is_horizontal(b):
            all_xy_pos = get_all_pos_for_horizontal_brick(b)
            to_add = set(grid[xy].get(s[2] - 1) for xy in all_xy_pos if grid[xy].get(s[2] - 1) is not None)
            for j in to_add:
                if j != -1:
                    supports.get(i).add(j)

        if is_vertical(b):
            j = grid[s[:2]][s[2] - 1]
            if j != -1:
                supports.get(i).add(j)

    return supports


def part_a(lines: List[str]) -> int:
    bricks = parse_snapshot(lines)
    grid = get_grid(bricks)
    settle_bricks(grid, bricks)
    supports = get_supports(grid, bricks)

    can_be_disintegrated = set()
    for i in bricks:
        is_only_support = False
        for j in [n for n in bricks if n != i]:
            if i in supports[j] and len(supports[j]) == 1:
                is_only_support = True
                break

        if not is_only_support:
            can_be_disintegrated.add(i)

    return len(can_be_disintegrated)


def part_b(lines: List[str]) -> int:
    bricks = parse_snapshot(lines)
    grid = get_grid(bricks)
    settle_bricks(grid, bricks)
    supports = get_supports(grid, bricks)

    killed_bricks = {}
    for i in bricks:
        bricks_killed = {i}
        while True:
            need_new_run = False
            to_check = [n for n in bricks if n not in bricks_killed]
            for j in to_check:
                if supports[j] != set() and supports[j].difference(bricks_killed) == set():
                    bricks_killed.add(j)
                    need_new_run = True
                    break

            if not need_new_run:
                break

        killed_bricks[i] = len(bricks_killed) - 1

    s = sum(l for _, l in killed_bricks.items())
    return s


def run() -> None:
    print("partA:")
    print(part_a(read_input_to_list(__file__)))
    assert part_a(read_input_to_list(__file__)) == 451
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 5

    print("partB:")
    print(part_b(read_input_to_list(__file__)))
    assert part_b(read_input_to_list(__file__)) == 66530
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 7

    print("done")
