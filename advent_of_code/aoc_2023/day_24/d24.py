import numpy as np
import sympy

from advent_of_code.commons.commons import read_input_to_list


def get_particles(lines: list[str]):
    particles = []
    for line in lines:
        p = line.split("@")
        pos = np.array([int(pos.strip()) for pos in p[0].split(",")])
        vel = np.array([int(pos.strip()) for pos in p[1].split(",")])
        particles.append((pos, vel))

    return particles


def intersection3d_point(p1: np.ndarray, m1: np.ndarray, p2: np.ndarray, m2: np.ndarray, eps=1e-6):
    # https://mathworld.wolfram.com/Line-LineIntersection.html
    assert len(p1) == len(p2) == len(m1) == len(m2) == 3
    m1_hat = m1 / np.linalg.norm(m1)
    m2_hat = m2 / np.linalg.norm(m2)
    c = p2 - p1
    v = np.cross(m1_hat, m2_hat)
    v_norm = np.linalg.norm(v)
    if abs(v_norm) < eps:
        return None

    v_hat = v / v_norm

    s1 = np.linalg.det(np.array([c, m2_hat, v_hat]).T) / v_norm**2
    s2 = np.linalg.det(np.array([c, m1_hat, v_hat]).T) / v_norm**2

    if s1 < 0 or s2 < 0:
        return None  # intersection in past of one of the lines

    return p1 + m1 * s1


def intersection2d_point(p1: np.ndarray, m1: np.ndarray, p2: np.ndarray, m2: np.ndarray, eps=1e-6):
    # https://en.wikipedia.org/wiki/Line–line_intersection
    assert len(p1) == len(p2) == len(m1) == len(m2) == 2
    c = p1 - p2

    a = np.array([c, -m2]).T
    a = np.linalg.det(a)
    b = np.array([-m1, -m2]).T
    b = np.linalg.det(b)
    if abs(b) < eps:
        return None

    t = a / b

    a = np.array([c, -m1]).T
    a = np.linalg.det(a)

    u = a / b

    if t < 0 or u < 0:
        # intersection lies in past
        return None

    return p1 + m1 * t


def intersection_point(p1, m1, p2, m2):
    if len(p1) == 2:
        return intersection2d_point(p1, m1, p2, m2)
    elif len(p1) == 3:
        return intersection3d_point(p1, m1, p2, m2)
    else:
        raise ValueError("Inputs must be 2D or 3D")


def compute_x(particle, t, t0):
    p1, v1 = particle
    x = v1 * (t - t0) + p1
    return x


def in_xy_boundary(x, area_min_max: tuple[int, int]):
    return area_min_max[0] <= x[0] <= area_min_max[1] and area_min_max[0] <= x[1] <= area_min_max[1]


def part_a(lines: list[str], area_min_max: tuple[int, int]) -> int:
    particles = get_particles(lines)
    particles_meet = []
    for i in range(len(particles) - 1):
        for j in range(i + 1, len(particles)):
            p1 = particles[i]
            p2 = particles[j]
            x1 = intersection_point(p1[0][:2], p1[1][:2], p2[0][:2], p2[1][:2])
            if x1 is None:
                continue
            if in_xy_boundary(x1, area_min_max):
                particles_meet.append((i, j))

    return len(particles_meet)


def part_b(lines: list[str]) -> int:
    particles = get_particles(lines)

    # symbolic solution
    x, y, z, dx, dy, dz = sympy.symbols("x y z dx dy dz")
    eqs = []
    for p in particles[:4]:
        a, b, c = p[0]
        da, db, dc = p[1]
        eqs.append(sympy.Eq((dy - db) * (a - x), (b - y) * (dx - da)))
        eqs.append(sympy.Eq((dz - dc) * (b - y), (c - z) * (dy - db)))

    sol = sympy.solve(eqs, [x, y, z, dx, dy, dz])
    assert len(sol) == 1
    res = sum(sol[0][:3])
    return res


def run() -> None:
    print("partA:")
    res = part_a(read_input_to_list(__file__), (200000000000000, 400000000000000))
    print(res)
    assert res == 29142
    assert part_a(read_input_to_list(__file__, read_test_input=True), (7, 27)) == 2

    print("partB:")
    res = part_b(read_input_to_list(__file__))
    print(res)
    assert res == 848947587263033
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 47

    print("done")
