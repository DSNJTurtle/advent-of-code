import shapely.geometry
from aocd.models import Puzzle, User
from shapely.geometry.polygon import Polygon


def part_a(input_data: str) -> str:
    return compute(input_data, False)


def part_b(input_data: str) -> str:
    return compute(input_data, True)


def compute(input_data: str, is_b: bool) -> str:
    tiles = [tuple(x.split(",")) for x in input_data.splitlines()]
    tiles = [int(a) + int(b) * 1j for a, b in tiles]

    p = Polygon([(x.real, x.imag) for x in tiles])

    thin_boxes = []
    normal_boxes = []
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            a = tiles[i]
            b = tiles[j]
            # thin rectangles
            if a.real == b.real or a.imag == b.imag:
                thin_boxes.append((a, b))
            else:
                normal_boxes.append((a, b))

    ma_thin_boxes = 0
    for a, b in thin_boxes:
        if abs(a - b) + 1 > ma_thin_boxes:
            ma_thin_boxes = abs(a - b) + 1

    ma_normal_boxes = 0
    for a, b in normal_boxes:
        area = (abs(a.real - b.real) + 1) * (abs(a.imag - b.imag) + 1)
        if is_b:
            b = shapely.geometry.box(min(a.real, b.real), min(a.imag, b.imag), max(a.real, b.real), max(a.imag, b.imag))
            c = p.contains(b)
        else:
            c = True

        if c and area > ma_normal_boxes:
            ma_normal_boxes = area

    return str(int(max(ma_thin_boxes, ma_normal_boxes)))


if __name__ == "__main__":
    token = ""
    p = Puzzle(2025, 9, user=User(token=token))

    if True:
        r = part_a(p.examples[0].input_data)
        print(f"Part A - Example Answer: {r}")
        # assert r == str(p.examples[0].answer_a)
        r = part_a(p.input_data)
        print(f"Part A - Answer: {r}")
        p.answer_a = r

    if True:
        r = part_b(p.examples[0].input_data)
        print(f"Part B - Example Answer: {r}")
        # assert r == p.examples[0].answer_b
        r = part_b(p.input_data)
        print(f"Part B - Answer: {r}")
        p.answer_b = r
