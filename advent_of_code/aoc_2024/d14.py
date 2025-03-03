import re
from dataclasses import dataclass
from numbers import Complex

import numpy as np

from advent_of_code.commons.commons import read_input_to_list


@dataclass
class Robot:
    """Robot class."""

    pos: Complex
    vel: Complex


def parse(lines: list[str]) -> list[Robot]:
    robots = []
    p = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")
    for line in lines:
        px, py, vx, vy = p.match(line).groups()
        robots.append(Robot(pos=int(px) + int(py) * 1j, vel=int(vx) + int(vy) * 1j))

    return robots


def modulo(x: int, y: int) -> int:
    if x >= 0:
        return x % y

    f = np.floor(x / y)
    return x - f * y


def solve(robots: list[Robot], grid_size: tuple[int, int], n_steps: int) -> list[Complex]:
    positions = [x.pos + n_steps * x.vel for x in robots]
    positions = [modulo(x.real, grid_size[0]) + modulo(x.imag, grid_size[1]) * 1j for x in positions]

    return positions


def get_quadrants(positions: list[Complex], dx: int, dy: int) -> tuple[int, int, int, int]:
    q1 = [x for x in positions if x.real < dx and x.imag < dy]
    q2 = [x for x in positions if x.real > dx and x.imag < dy]
    q3 = [x for x in positions if x.real < dx and x.imag > dy]
    q4 = [x for x in positions if x.real > dx and x.imag > dy]

    return len(q1), len(q2), len(q3), len(q4)


def part_a(lines: list[str], grid_size: tuple[int, int], n_steps: int) -> int:
    robots = parse(lines)
    positions = solve(robots, grid_size, n_steps)
    q1, q2, q3, q4 = get_quadrants(positions, grid_size[0] // 2, grid_size[1] // 2)
    return q1 * q2 * q3 * q4


def visualize(grid_size: tuple[int, int], positions: list[Complex]) -> None:
    grid = {x for x in positions}
    for x in range(grid_size[0]):
        for y in range(grid_size[1]):
            if x + y * 1j in grid:
                print("#", end="")
            else:
                print(".", end="")
        print()


def part_b(lines: list[str], grid_size: tuple[int, int]) -> int:
    robots = parse(lines)

    for i in range(20000000):
        positions = solve(robots, grid_size, i)
        x_pos = [x.real for x in positions]
        y_pos = [x.imag for x in positions]
        s_x = np.std(x_pos)
        s_y = np.std(y_pos)
        if s_x < 20 and s_y < 20:
            print(f"i: {i}")
            visualize(grid_size, positions)
            return i


def run() -> None:
    print("partA:")
    res = part_a(read_input_to_list(__file__), (101, 103), 100)
    print(res)
    assert res == 217132650
    assert part_a(read_input_to_list(__file__, read_test_input=True), (11, 7), 100) == 12

    print("partB:")
    res = part_b(read_input_to_list(__file__), (101, 103))
    print(res)
    assert res == 6516
    # assert part_b(read_input_to_list(__file__, read_test_input=True)) == 0

    print("done")
