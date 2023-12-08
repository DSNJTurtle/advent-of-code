from typing import List

from aoc_2023.commons.commons import read_input_to_list


def assign_hand_global_rank(hand: str) -> (int, int):
    assign_num_values = {"A": "14", "K": "13", "Q": "12", "J": "11", "T": "10"}

    occurrences = {}
    for c in ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]:
        occurrences[c] = hand.count(c)

    # tie breaker
    lower_mask = 0
    for i, s in enumerate(hand[::-1]):
        n = int(assign_num_values.get(s, s))
        lower_mask += pow(14, i) * n

    # top hand
    values = occurrences.values()
    if 5 in values:
        upper_mask = 2**6
    elif 4 in values:
        upper_mask = 2**5
    elif 3 in values:
        # full house
        if len([x for x in values if x >= 2]) > 1:
            upper_mask = 2**4
        else:
            # three of a kind
            upper_mask = 2**3
    elif len([x for x in values if x == 2]) > 1:
        upper_mask = 2**2
    elif 2 in values:
        upper_mask = 2**1
    else:
        upper_mask = 0

    return upper_mask, lower_mask


def assign_hand_global_rank_partb(hand: str) -> (int, int):
    assign_num_values = {"A": "14", "K": "13", "Q": "12", "J": "1", "T": "10"}

    occurrences = {}
    for c in ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]:
        occurrences[c] = hand.count(c)

    # tie breaker
    lower_mask = 0
    for i, s in enumerate(hand[::-1]):
        n = int(assign_num_values.get(s, s))
        lower_mask += pow(14, i) * n

    # top hand
    n_jokers = occurrences.get("J", 0)
    del occurrences["J"]

    values = occurrences.values()
    if n_jokers == 5 or (5 - n_jokers) in values:
        upper_mask = 2**6
    elif n_jokers == 4 or (4 - n_jokers) in values:
        upper_mask = 2**5
    elif n_jokers == 3 or (3 - n_jokers) in values:
        # full house
        if n_jokers <= 1 and len([x for x in values if x >= 2]) > 1:
            upper_mask = 2**4
        else:
            # three of a kind
            upper_mask = 2**3
    elif n_jokers + len([x for x in values if x == 2]) > 1:
        upper_mask = 2**2
    elif n_jokers + len([x for x in values if x == 2]) > 0 in values:
        upper_mask = 2**1
    else:
        upper_mask = 0

    return upper_mask, lower_mask


def parse(lines: List[str]):
    hands = []
    for i, l in enumerate(lines):
        p = l.strip().split()
        hand = p[0].strip()
        hands.append((i, hand, p[1].strip(), assign_hand_global_rank(hand)))

    return hands


def parse_b(lines: List[str]):
    hands = []
    for i, l in enumerate(lines):
        p = l.strip().split()
        hand = p[0].strip()
        hands.append((i, hand, p[1].strip(), assign_hand_global_rank_partb(hand)))

    return hands


def part_a(lines: List[str]) -> int:
    hands = parse(lines)
    hands.sort(key=lambda x: x[3], reverse=True)
    hands.reverse()

    winnings = 0
    for i, h in enumerate(hands):
        winnings += (i + 1) * int(h[2])

    return winnings


def part_b(lines: List[str]) -> int:
    hands = parse_b(lines)
    hands.sort(key=lambda x: x[3], reverse=True)
    hands.reverse()

    winnings = 0
    for i, h in enumerate(hands):
        winnings += (i + 1) * int(h[2])

    return winnings


def run() -> None:
    print("partA:")
    print(part_a(read_input_to_list(__file__)))
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 6440

    print("partB:")
    print(part_b(read_input_to_list(__file__)))
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 5905

    print("done")
