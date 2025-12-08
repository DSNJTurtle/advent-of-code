from aocd.models import Puzzle, User


def get_beam_col_positions(row: list[str]) -> list[int]:
    positions = []
    for i, c in enumerate(row):
        if c == "|":
            positions.append(i)

    return positions


def get_beam_col_positions_b(row: list[str]) -> list[int]:
    positions = []
    for i, c in enumerate(row):
        if c.isdigit():
            positions.append(i)

    return positions


def part_a(input_data: str) -> str:
    grid = [list(x) for x in input_data.splitlines()]

    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if col == "S":
                grid[i][j] = "|"

    # fill grid with beams
    for i, row in enumerate(grid):
        cols = get_beam_col_positions(row)
        if i == len(grid) - 1:
            # reached end of grid
            break

        for j in cols:
            c = grid[i + 1][j]
            if c == "^":
                if 0 <= j - 1 < len(grid[0]) and grid[i + 1][j - 1] != "^":
                    grid[i + 1][j - 1] = "|"
                if 0 <= j + 1 < len(grid[0]) and grid[i + 1][j + 1] != "^":
                    grid[i + 1][j + 1] = "|"
            elif c == ".":
                grid[i + 1][j] = "|"
            elif c == "|":
                continue
            else:
                raise ValueError(f"unknown operator: {c}")

    # count all splitters with a beam on top
    n_splits = 0
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c == "^" and grid[i - 1][j] == "|":
                n_splits += 1

    return str(n_splits)


def part_b(input_data: str) -> str:
    grid = [list(x) for x in input_data.splitlines()]

    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if col == "S":
                grid[i][j] = "1"

    # fill grid with beams
    for i, row in enumerate(grid):
        cols = get_beam_col_positions_b(row)
        if i == len(grid) - 1:
            # reached end of grid
            break

        for j in cols:
            n = 1 if grid[i][j] == "." else int(grid[i][j])
            ns = str(n)
            c = grid[i + 1][j]
            if c == "^":
                if 0 <= j - 1 < len(grid[0]) and grid[i + 1][j - 1] != "^":
                    grid[i + 1][j - 1] = ns if grid[i + 1][j - 1] == "." else str(int(grid[i + 1][j - 1]) + int(ns))
                if 0 <= j + 1 < len(grid[0]) and grid[i + 1][j + 1] != "^":
                    grid[i + 1][j + 1] = ns if grid[i + 1][j + 1] == "." else str(int(grid[i + 1][j + 1]) + int(ns))
            else:
                grid[i + 1][j] = ns if grid[i + 1][j] == "." else str(int(grid[i + 1][j]) + int(ns))

    # sum up final result
    n_splits = 0
    for _, c in enumerate(grid[-1]):
        if c.isdigit():
            n_splits += int(c)

    return str(n_splits)


if __name__ == "__main__":
    token = ""
    p = Puzzle(2025, 7, user=User(token=token))

    if True:
        r = part_a(p.examples[0].input_data)
        print(f"Part A - Example Answer: {r}")
        assert r == p.examples[0].answer_a
        r = part_a(p.input_data)
        print(f"Part A - Answer: {r}")
        p.answer_a = r

    if True:
        r = part_b(p.examples[0].input_data)
        print(f"Part B - Example Answer: {r}")
        assert r == p.examples[0].answer_b
        r = part_b(p.input_data)
        print(f"Part B - Answer: {r}")
        p.answer_b = r
