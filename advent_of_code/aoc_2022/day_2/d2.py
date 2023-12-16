from typing import List

import numpy as np

from advent_of_code.commons.commons import read_input_to_list

part_a_assignment = {"X": "A", "Y": "B", "Z": "C"}
part_b_assignment = {
    "X": {"A": "C", "B": "A", "C": "B"},
    "Y": {"A": "A", "B": "B", "C": "C"},
    "Z": {"A": "B", "B": "C", "C": "A"},
}


def get_games(lines: List[str]):
    games = [l.strip().split() for l in lines]

    return games


def score_per_game(opponent: str, my: str) -> int:
    if my == "A":
        if opponent == "A":
            return 3 + 1
        elif opponent == "B":
            return 0 + 1
        else:
            return 6 + 1
    elif my == "B":
        if opponent == "A":
            return 6 + 2
        elif opponent == "B":
            return 3 + 2
        else:
            return 0 + 2
    elif my == "C":
        if opponent == "A":
            return 0 + 3
        elif opponent == "B":
            return 6 + 3
        else:
            return 3 + 3


def part_a(lines: List[str]) -> int:
    games = get_games(lines)
    scores = [score_per_game(g[0], part_a_assignment[g[1]]) for g in games]

    return np.sum(scores)


def part_b(lines: List[str]) -> int:
    games = get_games(lines)
    scores = [score_per_game(g[0], part_b_assignment[g[1]][g[0]]) for g in games]

    return np.sum(scores)


def run() -> None:
    print("partA:")
    assert part_a(read_input_to_list(__file__)) == 13052
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 15

    print("partB:")
    assert part_b(read_input_to_list(__file__)) == 13693
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 12

    print("done")
