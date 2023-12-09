from typing import List

from aoc_2022.commons.commons import read_input_to_list


def parse_seq(seq: str, req_length: int) -> int:
    w = []
    for i in range(len(seq)):
        w.append(seq[i])
        if len(w) > req_length:
            w = w[1:]
        l = len(w)
        if l >= req_length and l == len(set(w)):
            return i + 1

    raise RuntimeError("failed")


def part_a(lines: List[str]) -> int:
    # tests
    assert parse_seq("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 4) == 7
    assert parse_seq("bvwbjplbgvbhsrlpgdmjqwftvncz", 4) == 5
    assert parse_seq("nppdvjthqldpwncqszvftbrmjlhg", 4) == 6
    assert parse_seq("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 4) == 10
    assert parse_seq("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 4) == 11

    n = parse_seq(lines[0], 4)

    return n


def part_b(lines: List[str]) -> int:
    # tests
    assert parse_seq("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14) == 19
    assert parse_seq("bvwbjplbgvbhsrlpgdmjqwftvncz", 14) == 23
    assert parse_seq("nppdvjthqldpwncqszvftbrmjlhg", 14) == 23
    assert parse_seq("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 14) == 29
    assert parse_seq("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 14) == 26

    n = parse_seq(lines[0], 14)

    return n


def run() -> None:
    print("partA:")
    assert part_a(read_input_to_list(__file__)) == 1155

    print("partB:")
    assert part_b(read_input_to_list(__file__)) == 2789

    print("done")
