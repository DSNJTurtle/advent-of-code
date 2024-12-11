import re
from dataclasses import dataclass

from advent_of_code.commons.commons import read_input_to_list


@dataclass
class Orientations:
    """Orientations."""

    rows: list[list[str]]
    cols: list[list[str]]
    fdiag: list[list[str]]
    bdiag: list[list[str]]

    def get_all(self) -> list[list[list[str]]]:
        return [self.rows, self.cols, self.fdiag, self.bdiag]


def all_orientations(m: list[list[str]]) -> Orientations:
    """Taken from https://stackoverflow.com/questions/6313308/get-all-the-diagonals-in-a-matrix-list-of-lists-in-python ."""
    max_col = len(m[0])
    max_row = len(m)
    cols = [[] for _ in range(max_col)]
    rows = [[] for _ in range(max_row)]
    fdiag = [[] for _ in range(max_row + max_col - 1)]
    bdiag = [[] for _ in range(len(fdiag))]
    min_bdiag = -max_row + 1

    for x in range(max_col):
        for y in range(max_row):
            cols[x].append(m[y][x])
            rows[y].append(m[y][x])
            fdiag[x + y].append(m[y][x])
            bdiag[x - y - min_bdiag].append(m[y][x])

    return Orientations(rows, cols, fdiag, bdiag)


def part_a(lines: list[str]) -> int:
    mat = []
    for x in lines:
        mat.append(list(x))

    p = re.compile(r"XMAS")
    n_occurances = 0
    orientations = all_orientations(mat)

    for o in orientations.get_all():
        for x in o:
            s = "".join(x)
            n_occurances += len(p.findall(s))
            n_occurances += len(p.findall(s[::-1]))

    return n_occurances


def get_submatrix(start_i: int, start_j: int, mat):
    res = []
    for i in range(start_i - 1, start_i + 2):
        res2 = []
        for j in range(start_j - 1, start_j + 2):
            res2.append(mat[i][j])

        res.append(res2)

    return res


def part_b(lines: list[str]) -> int:
    mat = []
    for x in lines:
        mat.append(list(x))

    n_occurances = 0
    # get all possible submatrices
    for i in range(1, len(mat) - 1):
        for j in range(1, len(mat[0]) - 1):
            sub_mat = get_submatrix(i, j, mat)

            # check for X-MAS
            if (
                (
                    sub_mat[0][0] == "M"
                    and sub_mat[0][2] == "S"
                    and sub_mat[1][1] == "A"
                    and sub_mat[2][0] == "M"
                    and sub_mat[2][2] == "S"
                )
                or (
                    sub_mat[0][0] == "S"
                    and sub_mat[0][2] == "S"
                    and sub_mat[1][1] == "A"
                    and sub_mat[2][0] == "M"
                    and sub_mat[2][2] == "M"
                )
                or (
                    sub_mat[0][0] == "M"
                    and sub_mat[0][2] == "M"
                    and sub_mat[1][1] == "A"
                    and sub_mat[2][0] == "S"
                    and sub_mat[2][2] == "S"
                )
                or (
                    sub_mat[0][0] == "S"
                    and sub_mat[0][2] == "M"
                    and sub_mat[1][1] == "A"
                    and sub_mat[2][0] == "S"
                    and sub_mat[2][2] == "M"
                )
            ):
                n_occurances += 1
            else:
                continue

    return n_occurances


def run() -> None:
    print("partA:")
    res = part_a(read_input_to_list(__file__))
    print(res)
    assert res == 2514
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 18

    print("partB:")
    res = part_b(read_input_to_list(__file__))
    print(res)
    assert res == 1888
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 9

    print("done")
