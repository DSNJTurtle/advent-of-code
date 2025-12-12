from dataclasses import dataclass

import numpy as np
from aocd.models import Puzzle, User
from scipy.optimize import LinearConstraint, milp


@dataclass
class Machine:
    """Machine."""

    state: list[int]
    buttons: list[list[int]]
    joltages: list[int]

    @classmethod
    def from_str(cls, line: str) -> "Machine":
        parts = line.split("]")
        m = [int(x) for x in list(parts[0].replace("[", "").replace(".", "0").replace("#", "1"))]
        parts = parts[1].split("{")
        b = parts[0].strip().split()
        b = [eval(x) for x in b]
        b = [list(x) if isinstance(x, tuple) else [x] for x in b]
        joltages = parts[1].replace("}", "").strip().split(",")
        joltages = [int(x) for x in joltages]
        return Machine(m, b, joltages)


def to_vector(i: int, d: int):
    v = np.zeros(d, dtype=int)
    v[i] = 1
    return v


def part_a(input_data: str) -> str:
    data = [Machine.from_str(s) for s in input_data.splitlines()]

    results = 0
    for m in data:
        state = np.array(m.state, dtype=int)
        d = len(state)

        # The important part here is, that the boundaries of the LIP are given by b' = b mod 2.
        # we need to add d vectors that cover the mod 2 operation for each dimension
        # The resulting problem to solve is then Ax - 2*v1 - 2*v2- ... - 2*vd = b
        c = np.ones(len(m.buttons) + d, dtype=int)
        # no value of these auxiliary vectors contribute to the cost function
        c[len(m.buttons) :] = 0
        bl = bu = state
        A = []
        for b in m.buttons:
            a = np.array([to_vector(x, d) for x in b], dtype=int)
            a = np.sum(a, axis=0)
            A.append(a)
        # append mod 2 vectors
        for i in range(d):
            v = np.zeros(d, dtype=int)
            v[i] = -2
            A.append(v)
        A = np.transpose(A)
        A = np.array(A, dtype=int)

        cons = LinearConstraint(A, bl, bu)
        integrality = np.ones_like(c)
        res = milp(c=c, constraints=cons, integrality=integrality)
        # select only the buttons from the final result
        resx = res.x[: len(m.buttons)]

        results += np.sum(resx)

    return str(int(results))


def part_b(input_data: str) -> str:
    # part b is actually simpler because exactly solve for the equality with the joltages and do not the mod 2 operation
    data = [Machine.from_str(s) for s in input_data.splitlines()]

    results = 0
    for m in data:
        state = np.array(m.joltages, dtype=int)
        d = len(state)

        c = np.ones(len(m.buttons), dtype=int)
        bl = bu = state
        A = []
        for b in m.buttons:
            a = np.array([to_vector(x, d) for x in b], dtype=int)
            a = np.sum(a, axis=0)
            A.append(a)
        A = np.transpose(A)
        A = np.array(A, dtype=int)

        cons = LinearConstraint(A, bl, bu)
        integrality = np.ones_like(c)
        res = milp(c=c, constraints=cons, integrality=integrality)
        resx = res.x

        results += np.sum(resx)

    return str(int(results))


if __name__ == "__main__":
    token = ""
    p = Puzzle(2025, 10, user=User(token=token))

    if True:
        r = part_a(p.examples[0].input_data)
        print(f"Part A - Example Answer: {r}")
        assert r == str(p.examples[0].answer_a)
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
