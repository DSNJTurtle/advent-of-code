from aocd.models import Puzzle, User


def parse_inpt(input_data: str):
    it = iter(input_data.splitlines())
    shapes = {}
    regions = []
    while (line := next(it, None)) is not None:
        if "x" not in line:
            si = int(line.replace(":", "").strip())
            shape = []
            while (ll := next(it, None)) is not None and ll.strip() != "":
                shape.append(list(ll))

            shapes[si] = shape
        else:
            size, numbers = line.split(":", 1)
            nsize = [int(x) for x in size.replace("x", " ").split()]
            numbers = [int(x) for x in numbers.strip().split()]
            regions.append((nsize, numbers))

    areas = {}
    for k, v in shapes.items():
        n = 0
        for vv in v:
            for i in vv:
                n += 1 if i == "#" else 0
        areas[k] = n

    return shapes, regions, areas


def part_a(input_data: str) -> str:
    shapes, regions, areas = parse_inpt(input_data)

    n_fits = 0
    for size, shapes in regions:
        # check feasability
        req_area = 0
        for i, v in enumerate(shapes):
            req_area += v * areas[i]

        is_feasable = req_area <= size[0] * size[1]

        if is_feasable:
            n_fits += 1

    return str(n_fits)


def part_b(input_data: str) -> str:
    return ""


if __name__ == "__main__":
    token = ""
    p = Puzzle(2025, 12, user=User(token=token))

    if True:
        # r = part_a(p.examples[0].input_data)
        # print(f"Part A - Example Answer: {r}")
        # assert r == str(p.examples[0].answer_a)
        r = part_a(p.input_data)
        print(f"Part A - Answer: {r}")
        p.answer_a = r

    if True:
        # r = part_b(p.examples[0].input_data)
        # print(f"Part B - Example Answer: {r}")
        # assert r == str(p.examples[0].answer_b)
        # r = part_b(p.input_data)
        # print(f"Part B - Answer: {r}")
        p.answer_b = "Finish Decorating the North Pole"
