from collections import defaultdict

import numpy as np
from aocd.models import Puzzle, User
from scipy.spatial import distance_matrix


def part_a(input_data: str, n_connections: int) -> str:
    data = np.array([[int(x) for x in ll.split(",")] for ll in input_data.splitlines()])

    m = distance_matrix(data, data)
    m = np.where(m == 0, np.inf, m)
    ii = np.triu_indices_from(m)
    m[ii] = np.inf

    circuits = {tuple(d1.tolist()): i for i, d1 in enumerate(data)}
    next_circuit_id = len(data) + 1
    for _ in range(n_connections):
        i, j = np.unravel_index(np.argmin(m), m.shape)
        m[i, j] = np.inf
        p1 = data[i]
        p2 = data[j]

        id1 = circuits.get(tuple(p1))
        id2 = circuits.get(tuple(p2))

        # combine existing circuits
        fuses1 = [x for x, v in circuits.items() if v == id1]
        fuses2 = [x for x, v in circuits.items() if v == id2]
        for f in fuses1 + fuses2:
            circuits[f] = next_circuit_id
        next_circuit_id += 1

    cl = defaultdict(list)
    for k, v in circuits.items():
        cl[v].append(k)

    largest_cls = sorted([len(x) for x in cl.values()], reverse=True)[:3]

    return str(int(np.prod(largest_cls)))


def part_b(input_data: str) -> str:
    data = np.array([[int(x) for x in ll.split(",")] for ll in input_data.splitlines()])

    m = distance_matrix(data, data)
    m = np.where(m == 0, np.inf, m)
    ii = np.triu_indices_from(m)
    m[ii] = np.inf

    circuits = {tuple(d1.tolist()): i for i, d1 in enumerate(data)}
    next_circuit_id = len(data) + 1
    while True:
        i, j = np.unravel_index(np.argmin(m), m.shape)
        m[i, j] = np.inf
        p1 = data[i]
        p2 = data[j]

        id1 = circuits.get(tuple(p1))
        id2 = circuits.get(tuple(p2))

        # combine existing circuits
        fuses1 = [x for x, v in circuits.items() if v == id1]
        fuses2 = [x for x, v in circuits.items() if v == id2]
        for f in fuses1 + fuses2:
            circuits[f] = next_circuit_id
        next_circuit_id += 1

        if len(set(circuits.values())) == 1:
            return str(p1[0] * p2[0])


if __name__ == "__main__":
    token = ""
    p = Puzzle(2025, 8, user=User(token=token))

    if True:
        r = part_a(p.examples[0].input_data, 10)
        print(f"Part A - Example Answer: {r}")
        assert r == p.examples[0].answer_a
        r = part_a(p.input_data, 1000)
        print(f"Part A - Answer: {r}")
        p.answer_a = r

    if True:
        r = part_b(p.examples[0].input_data)
        print(f"Part B - Example Answer: {r}")
        assert r == p.examples[0].answer_b
        r = part_b(p.input_data)
        print(f"Part B - Answer: {r}")
        p.answer_b = r
