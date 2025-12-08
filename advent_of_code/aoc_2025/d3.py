import numpy as np
from aocd.models import Puzzle, User


def part_a(input_data: str) -> str:
    data = [list(x) for x in input_data.splitlines()]

    values = []
    for b in data:
        i1 = np.argmax(b)
        v1 = b[i1]

        if i1 == len(b) - 1:
            b2 = b[:-1]
            i2 = np.argmax(b2)
            v2 = b2[i2]
            v = v2 + v1
        else:
            b2 = b[i1 + 1 :].copy()
            i2 = np.argmax(b2)
            v2 = b2[i2]
            v = v1 + v2

        values.append(int(v))

    return str(sum(values))


def part_b(input_data: str) -> str:
    data = [list(x) for x in input_data.splitlines()]

    values = []
    for b in data:
        chars = []
        remaining_chars = 12
        _b = b.copy()
        while remaining_chars > 0:
            i, v = _argmax(_b[: -(remaining_chars - 1)] if remaining_chars - 1 > 0 else _b)
            chars.append(v)
            _b = _b[i + 1 :]
            remaining_chars -= 1
        values.append(int("".join(chars)))

    return str(sum(values))


def _argmax(a: list[str]) -> tuple[int, str]:
    i = 0
    v = a[0]
    for ii in range(1, len(a)):
        if a[ii] > v:
            v = a[ii]
            i = ii

    return i, v


if __name__ == "__main__":
    token = ""
    p = Puzzle(2025, 3, user=User(token=token))

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
