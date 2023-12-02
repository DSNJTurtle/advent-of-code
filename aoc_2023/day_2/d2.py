from typing import Dict, List

import numpy as np

from aoc_2023.commons.commons import read_input_to_list


def to_dict(lines: List[str]) -> Dict[int, Dict[str, Dict[str, int]]]:
    games = {}
    for l in lines:
        part1 = l.split(":")
        game_no = int(part1[0].replace("Game ", ""))
        games.update({game_no: {}})
        for si, s in enumerate(part1[1].split(";")):
            games[game_no].update({si: {}})
            for c in s.split(","):
                colors = c.strip().split(" ")
                games[game_no][si].update({colors[1]: int(colors[0])})

    return games


def part_a(lines: List[str]) -> int:
    required_cubes = {"red": 12, "green": 13, "blue": 14}
    games = to_dict(lines)
    valid_game_ids = []
    for g in games:
        sets_possible = True
        for s in games[g]:
            for c in games[g][s]:
                if games[g][s][c] > required_cubes.get(c, 0):
                    sets_possible = False

        if sets_possible:
            valid_game_ids.append(g)

    return np.sum(valid_game_ids)


def part_b(lines: List[str]) -> int:
    games = to_dict(lines)
    powers = []
    for g in games:
        min_red = np.max([games[g][s].get("red", 0) for s in games[g]])
        min_green = np.max([games[g][s].get("green", 0) for s in games[g]])
        min_blue = np.max([games[g][s].get("blue", 0) for s in games[g]])
        powers.append(min_red * min_blue * min_green)

    return np.sum(powers)


def run() -> None:
    print("partA:")
    print(part_a(read_input_to_list(__file__)))
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 8

    print("partB:")
    print(part_b(read_input_to_list(__file__)))
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 2286

    print("done")
