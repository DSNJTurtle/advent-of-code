from typing import List

import numpy as np

from advent_of_code.commons.commons import read_input_to_list


def parse_moves(lines: List[str]):
    moves = []  # each element is [n_moves, from_stack, to_stack]
    for l in lines:
        p = l.split("from")
        n_moves = int(p[0].replace("move", "").strip())
        p = p[1].split("to")
        from_stack = int(p[0].strip()) - 1
        to_stack = int(p[1].strip()) - 1

        moves.append([n_moves, from_stack, to_stack])

    return moves


def create_stack(lines: List[str], n_cols: int):
    create_rows = []
    for l in lines:
        row = []
        for col in range(n_cols):
            create = l[:4].strip().replace("[", "").replace("]", "")
            row.append(create)
            l = l[4:]
        create_rows.append(row)

    # create stacks
    stacks = []
    for c in range(n_cols):
        stack = []
        for i in range(len(create_rows) - 1, -1, -1):
            char = create_rows[i][c]
            if char != "":
                stack.append(char)

        stacks.append(stack)

    return stacks


def part_a(lines: List[str], number_line: int) -> str:
    create_lines = lines[:number_line]
    n_cols = np.max([int(s.strip()) for s in lines[number_line].split() if s.strip() != ""])
    moves_lines = lines[number_line + 2 :]
    moves = parse_moves(moves_lines)
    stacks = create_stack(create_lines, n_cols)

    for m in moves:
        fs = stacks[m[1]]
        ts = stacks[m[2]]
        for n in range(m[0]):
            ts.append(fs[-1])
            fs = fs[:-1]
            stacks[m[1]] = fs

    # top entries
    top_entries = "".join([s[-1] for s in stacks if len(s)])

    return top_entries


def part_b(lines: List[str], number_line: int) -> str:
    create_lines = lines[:number_line]
    n_cols = np.max([int(s.strip()) for s in lines[number_line].split() if s.strip() != ""])
    moves_lines = lines[number_line + 2 :]
    moves = parse_moves(moves_lines)
    stacks = create_stack(create_lines, n_cols)

    for m in moves:
        fs = stacks[m[1]]
        ts = stacks[m[2]]
        n = m[0]
        ts.extend(fs[-n:])
        fs = fs[:-n]
        stacks[m[1]] = fs

    # top entries
    top_entries = "".join([s[-1] for s in stacks if len(s)])

    return top_entries


def run() -> None:
    print("partA:")
    assert part_a(read_input_to_list(__file__), number_line=8) == "ZSQVCCJLL"
    assert part_a(read_input_to_list(__file__, read_test_input=True), number_line=3) == "CMZ"

    print("partB:")
    assert part_b(read_input_to_list(__file__), number_line=8) == "QZFJRWHGS"
    assert part_b(read_input_to_list(__file__, read_test_input=True), number_line=3) == "MCD"

    print("done")
