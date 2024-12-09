from advent_of_code.commons.commons import read_input_to_list


def part_a(lines: list[str]) -> int:
    rows = [[int(y) for y in x.split()] for x in lines]
    left = sorted([x[0] for x in rows])
    right = sorted([x[1] for x in rows])
    res = 0
    for x, y in zip(left, right, strict=False):
        res += max(x, y) - min(x, y)

    return res


def part_b(lines: list[str]) -> int:
    rows = [[int(y) for y in x.split()] for x in lines]
    left = [x[0] for x in rows]
    d = {x[0]: 0 for x in rows}
    for n in [x[1] for x in rows]:
        d[n] = d.get(n, 0) + 1

    s = 0
    for n in left:
        s += n * d[n]

    return s


def run() -> None:
    print("partA:")
    res = part_a(read_input_to_list(__file__))
    print(res)
    assert res == 1889772
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 11

    print("partB:")
    res = part_b(read_input_to_list(__file__))
    print(res)
    assert res == 23228917
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 31

    print("done")
