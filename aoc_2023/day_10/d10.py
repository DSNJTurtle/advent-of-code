"""Sorry, dirty code"""
from typing import List

import numpy as np

from aoc_2023.commons.commons import read_input_to_list


def parse(lines: List[str]):
    grid = []
    for l in lines:
        grid.append([str(s.strip()) for s in l])

    return grid


def find_start(grid):
    start_pos = None
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "S":
                start_pos = (i, j)
                break

        if start_pos is not None:
            break

    return start_pos


def create_loop(grid, start_pos):
    i, j = start_pos
    loop = [(i, j, grid[i][j])]
    # find first next tile
    assert 0 < i < len(grid) - 1  # start not at border
    if grid[i + 1][j] in ["|", "L", "J"]:
        loop.append((i + 1, j, grid[i + 1][j]))
    else:
        raise RuntimeError("Other input")

    while True:
        curr_pos = loop[-1]
        prev_pos = loop[-2]
        move_downwards = np.sign(curr_pos[0] - prev_pos[0]) * 1  # +1 if moving down
        move_right = np.sign(curr_pos[1] - prev_pos[1]) * 1  # +1 if moving to the right
        if curr_pos[-1] == "|":
            i, j = (curr_pos[0] + move_downwards, curr_pos[1])
        elif curr_pos[-1] == "-":
            i, j = (curr_pos[0], curr_pos[1] + move_right)
        elif curr_pos[-1] == "L":
            if move_downwards > 0:
                i, j = (curr_pos[0], curr_pos[1] + 1)
            else:
                i, j = (curr_pos[0] - 1, curr_pos[1])
        elif curr_pos[-1] == "J":
            if move_downwards > 0:
                i, j = (curr_pos[0], curr_pos[1] - 1)
            else:
                i, j = (curr_pos[0] - 1, curr_pos[1])
        elif curr_pos[-1] == "7":
            if move_right > 0:
                i, j = (curr_pos[0] + 1, curr_pos[1])
            else:
                i, j = (curr_pos[0], curr_pos[1] - 1)
        elif curr_pos[-1] == "F":
            if move_right < 0:
                i, j = (curr_pos[0] + 1, curr_pos[1])
            else:
                i, j = (curr_pos[0], curr_pos[1] + 1)
        else:
            raise RuntimeError("unknown pos")

        s = grid[i][j]
        if s == "S":
            break
        loop.append((i, j, s))

    return loop


def part_a(lines: List[str]) -> int:
    grid = parse(lines)
    start_pos = find_start(grid)
    loop = create_loop(grid, start_pos)

    l = len(loop)

    return l // 2


def moving_direction(prev_pos, curr_pos) -> str:
    ai = prev_pos[0]
    aj = prev_pos[1]
    bi = curr_pos[0]
    bj = curr_pos[1]
    if bi - ai == 0 and bj - aj == -1:
        return "L"
    if bi - ai == 0 and bj - aj == 1:
        return "R"
    if bi - ai == 1 and bj - aj == 0:
        return "D"
    if bi - ai == -1 and bj - aj == 0:
        return "U"

    raise RuntimeError("Unknown movement")


def part_b(lines: List[str], is_ccw: bool) -> int:
    grid = parse(lines)
    start_pos = find_start(grid)
    loop = create_loop(grid, start_pos)
    area = np.array([[0] * len(grid[0]) for _ in range(len(grid))])
    counter = 5
    for i, j, _ in loop:
        area[i][j] = counter
        counter += 1

    if is_ccw:
        # ccw
        for i in range(len(loop)):
            prev_pos = loop[i - 1]
            curr_pos = loop[i]
            m = curr_pos[0]
            n = curr_pos[1]
            if m - prev_pos[0] == 0 and n - prev_pos[1] == -1:
                # moving left
                col = area[:, n]
                for a_i in range(m + 1, len(col)):
                    if area[a_i][n] < 5:
                        area[a_i][n] = 1
                    else:
                        break
            elif m - prev_pos[0] == 0 and n - prev_pos[1] == 1:
                # moving right
                col = area[:, n]
                for a_i in range(m - 1, -1, -1):
                    if area[a_i][n] < 5:
                        area[a_i][n] = 1
                    else:
                        break
            elif m - prev_pos[0] == 1 and n - prev_pos[1] == 0:
                # moving down
                row = area[m]
                for a_j in range(n + 1, len(row)):
                    if area[m][a_j] < 5:
                        area[m][a_j] = 1
                    else:
                        break
            elif m - prev_pos[0] == -1 and n - prev_pos[1] == 0:
                # moving up
                row = area[m]
                for a_j in range(n - 1, -1, -1):
                    if area[m][a_j] < 5:
                        area[m][a_j] = 1
                    else:
                        break
            else:
                raise RuntimeError("unknown moving direction")
    else:
        # cw
        for i in range(len(loop)):
            prev_pos = loop[i - 1]
            curr_pos = loop[i]
            next_pos = loop[(i + 1) % len(loop)]
            m = curr_pos[0]
            n = curr_pos[1]
            move = moving_direction(prev_pos, curr_pos)
            next_move = moving_direction(curr_pos, next_pos)
            if move == "R":
                # moving right
                # looking down
                col = area[:, n]
                for a_i in range(m + 1, len(col)):
                    if area[a_i][n] < 5:
                        area[a_i][n] = 1
                    else:
                        break
                # looking right in case of edge
                if next_move == "U":
                    for a_j in range(n + 1, len(area[m])):
                        if area[m][a_j] < 5:
                            area[m][a_j] = 1
                        else:
                            break
            elif move == "L":
                # moving left
                # looking up
                for a_i in range(m - 1, -1, -1):
                    if area[a_i][n] < 5:
                        area[a_i][n] = 1
                    else:
                        break
                # looking left in case of edge
                if next_move == "D":
                    for a_j in range(n - 1, -1, -1):
                        if area[m][a_j] < 5:
                            area[m][a_j] = 1
                        else:
                            break
            elif move == "U":
                # moving up
                # looking right
                row = area[m]
                for a_j in range(n + 1, len(row)):
                    if area[m][a_j] < 5:
                        area[m][a_j] = 1
                    else:
                        break
                # looking up in case of edge
                if next_move == "L":
                    for a_i in range(m - 1, -1, -1):
                        if area[a_i][n] < 5:
                            area[a_i][n] = 1
                        else:
                            break
            elif move == "D":
                # moving down
                # looking left
                for a_j in range(n - 1, -1, -1):
                    if area[m][a_j] < 5:
                        area[m][a_j] = 1
                    else:
                        break
                # looking down in case of edge
                if next_move == "R":
                    for a_i in range(m + 1, len(area[:, n])):
                        if area[a_i][n] < 5:
                            area[a_i][n] = 1
                        else:
                            break
            else:
                raise RuntimeError("unknown moving direction")

    n_tiles = np.sum(area == 1)

    return n_tiles


def run() -> None:
    print("partA:")
    assert part_a(read_input_to_list(__file__)) == 6768
    assert part_a(read_input_to_list(__file__, filename="test2.txt", read_test_input=True)) == 4
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 8

    print("partB:")
    assert part_b(read_input_to_list(__file__), is_ccw=False) == 351
    assert part_b(read_input_to_list(__file__, filename="testB.txt", read_test_input=True), is_ccw=True) == 4
    assert (
        part_b(read_input_to_list(__file__, filename="testB2.txt", read_test_input=True), is_ccw=False) == 8
    )
    # assert part_b(read_input_to_list(__file__, filename="testB3.txt", read_test_input=True), is_ccw=False) == 10

    print("done")
