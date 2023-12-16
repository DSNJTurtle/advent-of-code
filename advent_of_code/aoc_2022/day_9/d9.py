from typing import List, Tuple

import numpy as np

from advent_of_code.commons.commons import read_input_to_list


def parse(lines: List[str]):
    moves = []
    for l in lines:
        p = l.split()
        moves.append([p[0].strip(), int(p[1].strip())])

    return moves


def to_pair(pos):
    return pos[0], pos[1]


def update_next_chain_element(head_pos, tail_pos) -> None | Tuple[int, int]:
    row_offset = head_pos[0] - tail_pos[0]
    col_offset = head_pos[1] - tail_pos[1]

    if abs(row_offset) > 2 or abs(col_offset) > 2:
        raise RuntimeError("Invalid move")

    if row_offset == 0 and col_offset == 2:
        return tail_pos[0], tail_pos[1] + 1

    if row_offset == 0 and col_offset == -2:
        return tail_pos[0], tail_pos[1] - 1

    if col_offset == 0 and row_offset == 2:
        return tail_pos[0] + 1, tail_pos[1]

    if col_offset == 0 and row_offset == -2:
        return tail_pos[0] - 1, tail_pos[1]

    if row_offset == 2 and 0 < abs(col_offset) <= 2:
        # diagonal up
        return tail_pos[0] + 1, tail_pos[1] + np.sign(col_offset) * 1

    if row_offset == -2 and 0 < abs(col_offset) <= 2:
        # diagonal down
        return tail_pos[0] - 1, tail_pos[1] + np.sign(col_offset) * 1

    if col_offset == -2 and 0 < abs(row_offset) <= 2:
        # diagonal left
        return tail_pos[0] + np.sign(row_offset) * 1, tail_pos[1] - 1

    if col_offset == 2 and 0 < abs(row_offset) <= 2:
        # diagonal right
        return tail_pos[0] + np.sign(row_offset) * 1, tail_pos[1] + 1

    return None


def part_a(lines: List[str]) -> int:
    moves = parse(lines)
    visited_pos = []
    chain = [[0, 0], [0, 0]]
    head_pos = chain[0]
    tail_pos = chain[-1]
    visited_pos.append(to_pair(tail_pos))

    for m in moves:
        for i in range(m[1]):
            if m[0] == "U":
                head_pos[0] += 1
            elif m[0] == "D":
                head_pos[0] -= 1
            elif m[0] == "L":
                head_pos[1] -= 1
            else:
                head_pos[1] += 1

            new_pos = update_next_chain_element(head_pos, tail_pos)
            if new_pos is not None:
                visited_pos.append(new_pos)
                tail_pos[0] = new_pos[0]
                tail_pos[1] = new_pos[1]

    return len(set(visited_pos))


def print_chain(chain, n_rows, n_cols) -> None:
    grid = ["." * n_cols for _ in range(n_rows)]
    for i in range(len(chain) - 1, -1, -1):
        if i == 0:
            s = "H"
        else:
            s = str(i)

        e = chain[i]
        old_s = grid[e[0]]
        grid[e[0]] = old_s[: e[1]] + s + old_s[e[1] + 1 :]

    grid.reverse()
    for s in grid:
        print(s)
    print()
    print()


def part_b(lines: List[str]) -> int:
    moves = parse(lines)
    visited_pos = []
    chain = [[0, 0] for _ in range(10)]
    visited_pos.append(to_pair(chain[-1]))

    # print_chain(chain, 5, 6)

    for m in moves:
        for i in range(m[1]):
            if m[0] == "U":
                chain[0][0] += 1
            elif m[0] == "D":
                chain[0][0] -= 1
            elif m[0] == "L":
                chain[0][1] -= 1
            else:
                chain[0][1] += 1

            for i in range(1, len(chain)):
                h = chain[i - 1]
                t = chain[i]
                new_pos = update_next_chain_element(h, t)
                if new_pos is not None:
                    if i == len(chain) - 1:
                        visited_pos.append(new_pos)
                    t[0] = new_pos[0]
                    t[1] = new_pos[1]

            # print_chain(chain, 5, 6)

    return len(set(visited_pos))


def run() -> None:
    print("partA:")
    assert part_a(read_input_to_list(__file__)) == 6337
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 13

    print("partB:")
    assert part_b(read_input_to_list(__file__)) == 2455
    assert part_b(read_input_to_list(__file__, filename="test2.txt", read_test_input=True)) == 36

    print("done")
