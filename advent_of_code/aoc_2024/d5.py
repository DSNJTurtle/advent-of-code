from functools import cmp_to_key, partial

from advent_of_code.commons.commons import read_input_to_list

page_order_dict = dict[int, list[int]]
page = list[int]


def split_input(lines: list[str]) -> tuple[page_order_dict, page_order_dict, list[page]]:
    ordering = {}
    pages = []
    for x in lines:
        if "|" in x:
            p = x.split("|")
            k = int(p[0])
            v = int(p[1])
            if (_v := ordering.get(k)) is not None:
                _v.append(v)
            else:
                ordering[k] = [v]
        elif "," in x:
            _x = [int(y) for y in x.split(",")]
            pages.append(_x)

    left_of, right_of = left_right_ordering(ordering)

    return left_of, right_of, pages


def left_right_ordering(left_of: page_order_dict) -> tuple[page_order_dict, page_order_dict]:
    right_of = {}
    for k, v in left_of.items():
        for x in v:
            if (_v := right_of.get(x)) is not None:
                _v.append(k)
            else:
                right_of[x] = [k]

    return left_of, right_of


def page_comparator(x: int, y: int, left_of: page_order_dict, right_of: page_order_dict) -> int:
    _r = right_of.get(x)
    _l = left_of.get(x)
    if _l is not None and y in _l:
        return -1
    if _r is not None and y in _r:
        return 1
    else:
        return 0


def part_a(lines: list[str]) -> int:
    left_of, right_of, pages = split_input(lines)
    cmp = partial(page_comparator, left_of=left_of, right_of=right_of)

    _sum = 0
    for p in pages:
        ordered_p = sorted(p, key=cmp_to_key(cmp))
        if p == ordered_p:
            i = len(ordered_p) // 2
            middle = ordered_p[i]
            _sum += middle

    return _sum


def part_b(lines: list[str]) -> int:
    left_of, right_of, pages = split_input(lines)
    cmp = partial(page_comparator, left_of=left_of, right_of=right_of)

    _sum = 0
    for p in pages:
        ordered_p = sorted(p, key=cmp_to_key(cmp))
        if p != ordered_p:
            i = len(ordered_p) // 2
            middle = ordered_p[i]
            _sum += middle

    return _sum


def run() -> None:
    print("partA:")
    res = part_a(read_input_to_list(__file__))
    print(res)
    assert res == 5955
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 143

    print("partB:")
    res = part_b(read_input_to_list(__file__))
    print(res)
    assert res == 4030
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 123

    print("done")
