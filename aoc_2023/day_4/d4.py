import math
from typing import Dict, List

import numpy as np

from aoc_2023.commons.commons import read_input_to_list


def to_dict(lines: List[str]):
    d = {}
    for l in lines:
        p1 = l.split(":")
        card_no = int(p1[0].split()[1])
        p2 = p1[1].split("|")
        winning_no = [int(s) for s in p2[0].strip().split()]
        my_no = [int(s) for s in p2[1].strip().split()]
        d.update({card_no: {"winning_no": winning_no, "my_no": my_no}})

    return d


def get_winning_cards_per_card(d, k) -> List[int]:
    wins = []
    for i in d[k]["my_no"]:
        if i in d[k]["winning_no"]:
            wins.append(i)

    return wins


def part_a(lines: List[str]) -> int:
    d = to_dict(lines)
    points = 0
    for k in d:
        wins = get_winning_cards_per_card(d, k)
        if wins:
            points += math.pow(2, len(wins) - 1)

    return int(points)


def part_b(lines: List[str]) -> int:
    d = to_dict(lines)

    total_cards_played: Dict[int, int] = {}  # {card: #cards}
    cards_to_play = {k: 1 for k in d}

    while cards_to_play:
        cur_no = list(sorted(cards_to_play.keys()))[0]
        n_cards = cards_to_play[cur_no]
        del cards_to_play[cur_no]

        wins = get_winning_cards_per_card(d, cur_no)
        new_cards = list(range(cur_no + 1, cur_no + len(wins) + 1)) if wins else []
        for c in new_cards:
            cards_to_play[c] = cards_to_play.get(c, 0) + 1 * n_cards

        total_cards_played[cur_no] = total_cards_played.get(cur_no, 0) + n_cards

    total_no_cards = np.sum(list(total_cards_played.values()))

    return total_no_cards


def run() -> None:
    print("partA:")
    print(part_a(read_input_to_list(__file__)))
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 13

    print("partB:")
    print(part_b(read_input_to_list(__file__)))
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 30

    print("done")
