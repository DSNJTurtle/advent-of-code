from typing import List, Tuple

from aoc_2023.commons.commons import read_input_to_list


def parse(lines: List[str]) -> List[Tuple[int, int]]:
    times = []
    distances = []
    for l in lines:
        if l.startswith("Time"):
            times = [int(s) for s in l.split(":")[1].strip().split()]
        elif l.startswith("Distance"):
            distances = [int(s) for s in l.split(":")[1].strip().split()]
        else:
            raise RuntimeError("error")

    result = list(zip(times, distances))

    return result


def part_a(lines: List[str]) -> int:
    td_list = parse(lines)
    wins_per_race = []

    for r in td_list:
        t = r[0]
        d = r[1]
        wins = 0
        for rt in range(t + 1):
            rd = rt * (t - rt)
            if rd > d:
                wins += 1

        wins_per_race.append(wins)

    n_wins = 1
    for i in wins_per_race:
        n_wins *= i

    return n_wins


def part_b(lines: List[str]) -> int:
    td_list = parse(lines)
    time = int("".join([str(t[0]) for t in td_list]))
    distance = int("".join([str(t[1]) for t in td_list]))

    # compute first winning time
    first_winning_time = 0
    last_winning_time = 0
    for rt in range(time + 1):
        rd = rt * (time - rt)
        if rd > distance:
            first_winning_time = rt
            break

    # compute last winning time
    for rt in range(time, 0, -1):
        rd = rt * (time - rt)
        if rd > distance:
            last_winning_time = rt
            break

    n_ways_to_win = last_winning_time - first_winning_time + 1

    return n_ways_to_win


def run() -> None:
    print("partA:")
    print(part_a(read_input_to_list(__file__)))
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 288

    print("partB:")
    print(part_b(read_input_to_list(__file__)))
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 71503

    print("done")
