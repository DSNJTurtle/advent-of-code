import numpy as np
from aocd.models import Puzzle, User


def part_a(input_data: str) -> str:
    data = {j + i * 1j: c for i, line in enumerate(input_data.splitlines()) for j, c in enumerate(line.split())}

    dim_lines = int(max(x.imag for x in data))
    dim_problems = int(max(x.real for x in data))

    results = []
    for p in range(dim_problems + 1):
        values = [p + ll * 1j for ll in range(dim_lines)]
        values = [int(data[x]) for x in values]
        op = data[p + dim_lines * 1j]

        if op == "+":
            r = sum(values)
        elif op == "*":
            r = int(np.prod(values))
        else:
            raise ValueError(f"unknown operator: {op}")

        results.append(r)

    return str(sum(results))


def part_b(input_data: str) -> str:
    data = [list(line) for line in input_data.splitlines()]

    n_numbers = len(data)

    results = []
    accum = []
    while data[0]:
        number = "".join([data[n].pop() for n in range(n_numbers - 1)]).strip()
        op = data[n_numbers - 1].pop().strip()
        if number == "":
            continue
        number = int(number)
        accum.append(number)
        if op == "":
            continue
        elif op == "*":
            results.append(int(np.prod(accum)))
            accum = []
        elif op == "+":
            results.append(int(sum(accum)))
            accum = []
        else:
            raise ValueError(f"unknown operator: {op}")

    return str(sum(results))


if __name__ == "__main__":
    token = ""
    p = Puzzle(2025, 6, user=User(token=token))

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
