import re
from dataclasses import dataclass
from numbers import Complex

from advent_of_code.commons.commons import read_input_to_list


@dataclass
class Machine:
    """Machine."""

    a: Complex
    b: Complex
    prize: Complex


def parse(lines: list[str]) -> list[Machine]:
    machines = []
    machine = Machine(a=0, b=0, prize=0)
    pattern = r".*: X\+(\d+), Y\+(\d+)"
    pattern2 = r".*: X\=(\d+), Y\=(\d+)"
    p = re.compile(pattern)
    p2 = re.compile(pattern2)
    for line in lines:
        if line.startswith("Button A:"):
            i, j = p.match(line).groups()
            machine.a = int(i) + int(j) * 1j
        elif line.startswith("Button B:"):
            i, j = p.match(line).groups()
            machine.b = int(i) + int(j) * 1j
        elif line.startswith("Prize:"):
            i, j = p2.match(line).groups()
            machine.prize = int(i) + int(j) * 1j
        else:
            machines.append(machine)
            machine = Machine(a=0, b=0, prize=0)

    # append last machine
    machines.append(machine)

    return machines


def solve(m: Machine) -> int:
    solutions = []
    # solution 1 - first n1, then n2
    denom = m.b.imag - m.b.real * m.a.imag / m.a.real
    n2 = 0 if abs(denom) < 1e-06 else round((m.prize.imag - m.prize.real * m.a.imag / m.a.real) / denom)
    n1 = round((m.prize.real - n2 * m.b.real) / m.a.real)
    res: Complex = n1 * m.a + n2 * m.b
    if res == m.prize:
        solutions.append((n1, n2))

    # solution 2 - first n2, then n1
    denom = m.a.real - m.a.real * m.b.imag / m.b.real
    n1 = 0 if abs(denom) < 1e-06 else round((m.prize.imag - m.prize.real * m.b.imag / m.b.real) / denom)
    n2 = round((m.prize.real - n1 * m.a.real) / m.b.real)
    res: Complex = n1 * m.a + n2 * m.b
    if res == m.prize:
        solutions.append((n1, n2))

    costs = [n1 * 3 + n2 for n1, n2 in solutions]
    return 0 if len(costs) == 0 else min(costs)


def part_a(lines: list[str]) -> int:
    machines = parse(lines)
    costs = [solve(m) for m in machines]
    return sum(costs)


def part_b(lines: list[str]) -> int:
    machines = parse(lines)
    machines = [Machine(a=m.a, b=m.b, prize=m.prize + 10000000000000 * (1 + 1j)) for m in machines]
    costs = [solve(m) for m in machines]
    return sum(costs)


def run() -> None:
    print("partA:")
    res = part_a(read_input_to_list(__file__))
    print(res)
    assert res == 34393
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 480

    print("partB:")
    res = part_b(read_input_to_list(__file__))
    print(res)
    assert res == 83551068361379
    # assert part_b(read_input_to_list(__file__, read_test_input=True)) == 0

    print("done")
