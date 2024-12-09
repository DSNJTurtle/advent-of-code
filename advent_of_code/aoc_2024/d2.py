import numpy as np

from advent_of_code.commons.commons import read_input_to_list


def is_report_safe(a) -> bool:
    a = np.asarray(a)
    a = np.diff(a, 1, axis=0)

    same_direction = np.all(a < 0) or np.all(a > 0)
    go = np.all(np.abs(a) >= 1)
    lt = np.all(np.abs(a) <= 3)

    return same_direction and go and lt


def part_a(lines: list[str]) -> int:
    levels = [[int(y) for y in x.split()] for x in lines]

    n_safe_levels = 0
    for level in levels:
        if is_report_safe(level):
            n_safe_levels += 1

    return n_safe_levels


def part_b(lines: list[str]) -> int:
    levels = [[int(y) for y in x.split()] for x in lines]

    n_safe_levels = 0
    for report in levels:
        safe_reports = [is_report_safe(report)]

        # array without one element
        for i in range(len(report)):
            new_report = np.delete(report, i)
            safe_reports.append(is_report_safe(new_report))

        if np.any(np.asarray(safe_reports)):
            n_safe_levels += 1

    return n_safe_levels


def run() -> None:
    print("partA:")
    res = part_a(read_input_to_list(__file__))
    print(res)
    assert res == 411
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 2

    print("partB:")
    res = part_b(read_input_to_list(__file__))
    print(res)
    assert res == 465
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 4

    print("done")
