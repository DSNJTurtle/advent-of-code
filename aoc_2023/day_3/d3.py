from typing import List

import numpy as np

from aoc_2023.commons.commons import read_input_to_list


def get_matrix(lines: List[str]) -> List[List[str]]:
    m = []
    for l in lines:
        incomplete_row = []
        cur_s = ""
        for s in l:
            if str(s).isdigit():
                cur_s += s

            else:
                if len(cur_s) > 0:
                    incomplete_row.append(cur_s)
                    cur_s = ""

                incomplete_row.append(s)

        if len(cur_s) > 0:  # number at end of row
            incomplete_row.append(cur_s)

        complete_row = []
        for p in incomplete_row:
            complete_row.extend([p] * len(p))

        m.append(complete_row)

    assert len(m) == len(lines)
    assert len(set([len(r) for r in m])) == 1

    return m


def get_nums_from_submatrix(m, i, j) -> List[str]:
    a = []
    for rr in m[np.max(i - 1, 0) : i + 2]:
        a.append(rr[np.max(j - 1, 0) : j + 2])

    assert len(a) == 3
    assert all([len(r) == 3 for r in a])

    res = []
    for ii in range(len(a)):
        res.extend(list(set([el for el in a[ii] if el.isnumeric()])))  # fails if we have `n.n`

    return res


def part_a(lines: List[str]) -> int:
    m = get_matrix(lines)
    assert len(m) == len(m[:][0])

    numbers = []
    for i in range(len(m)):
        for j in range(len(m[i])):
            e = m[i][j]
            if not e.isnumeric() and e != ".":
                res = get_nums_from_submatrix(m, i, j)
                numbers.extend(res)

    res = [int(e) for e in numbers]
    res = np.sum(res)

    return res


def part_b(lines: List[str]) -> int:
    m = get_matrix(lines)

    numbers = []
    for i in range(len(m)):
        for j in range(len(m[i])):
            e = m[i][j]
            if e == "*":
                res = get_nums_from_submatrix(m, i, j)
                if len(res) == 2:
                    numbers.append(int(res[0]) * int(res[1]))

    return np.sum(numbers)


def run() -> None:
    print("partA:")
    print(part_a(read_input_to_list(__file__)))
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 4361

    print("partB:")
    print(part_b(read_input_to_list(__file__)))
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 467835

    print("done")
