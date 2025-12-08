from aocd.models import Puzzle, User


def part_a(input_data: str) -> str:
    grid = {i + j * 1j: c for i, line in enumerate(input_data.splitlines()) for j, c in enumerate(line)}
    offset_pos = [i + j * 1j for i in range(-1, 2) for j in range(-1, 2) if i != 0 or j != 0]

    n_total_rolls = 0
    for k, v in grid.items():
        n_rolls = 0
        if v == "@":
            for pos in offset_pos:
                np = k + pos
                nv = grid.get(np, ".")
                n_rolls += 1 if nv == "@" else 0

            if n_rolls < 4:
                n_total_rolls += 1

    return str(n_total_rolls)


def part_b(input_data: str) -> str:
    grid = {i + j * 1j: c for i, line in enumerate(input_data.splitlines()) for j, c in enumerate(line)}
    offset_pos = [i + j * 1j for i in range(-1, 2) for j in range(-1, 2) if i != 0 or j != 0]

    rolls_iteration = []

    _i = 0
    while True:
        _i += 1
        print(f"Iteration {_i}")

        n_total_rolls = 0
        for k, v in grid.items():
            n_rolls = 0
            if v == "@":
                for pos in offset_pos:
                    np = k + pos
                    nv = grid.get(np, ".")
                    n_rolls += 1 if nv == "@" else 0

                if n_rolls < 4:
                    n_total_rolls += 1
                    grid[k] = "."

        if n_total_rolls == 0:
            break

        rolls_iteration.append(n_total_rolls)

    return str(sum(rolls_iteration))


if __name__ == "__main__":
    token = ""
    p = Puzzle(2025, 4, user=User(token=token))

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
