from typing import List

import numpy as np

from advent_of_code.commons.commons import read_input_to_list


def parse(lines: List[str]):
    grid = []
    for l in lines:
        grid.append([int(n) for n in l.strip()])

    return np.array(grid)


def part_a(lines: List[str]) -> int:
    grid = parse(lines)

    n_visible_trees = 0
    n_rows = len(grid)
    n_cols = len(grid[0])
    for i in range(n_rows):
        for j in range(n_cols):
            tree = grid[i, j]
            max_left = grid[i, :j]
            max_left = -1 if len(max_left) == 0 else np.max(max_left)
            max_right = grid[i, j + 1 :]
            max_right = -1 if len(max_right) == 0 else np.max(max_right)
            max_up = grid[:i, j]
            max_up = -1 if len(max_up) == 0 else np.max(max_up)
            max_down = grid[i + 1 :, j]
            max_down = -1 if len(max_down) == 0 else np.max(max_down)

            if tree > max_left or tree > max_right or tree > max_up or tree > max_down:
                n_visible_trees += 1

    return n_visible_trees


def viewing_distance(h: int, viewing_array: np.ndarray) -> int:
    distance = 0
    for i in range(len(viewing_array)):
        distance += 1
        if viewing_array[i] >= h:
            break

    return distance


def part_b(lines: List[str]) -> int:
    grid = parse(lines)
    scores = np.zeros(grid.shape)

    n_rows = len(grid)
    n_cols = len(grid[0])
    for i in range(n_rows):
        for j in range(n_cols):
            tree = int(grid[i, j])
            l = viewing_distance(tree, np.flip(grid[i, :j]))
            r = viewing_distance(tree, grid[i, j + 1 :])
            u = viewing_distance(tree, np.flip(grid[:i, j]))
            d = viewing_distance(tree, grid[i + 1 :, j])
            scores[i, j] = l * r * u * d

    return int(np.max(scores))


def run() -> None:
    print("partA:")
    assert part_a(read_input_to_list(__file__)) == 1805
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 21

    print("partB:")
    assert part_b(read_input_to_list(__file__)) == 444528
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 8

    print("done")
