from typing import Callable, List

import numpy as np

from advent_of_code.commons.commons import read_input_to_list


def parse(lines: List[str]):
    d = {}
    m = -1
    for l in lines:
        ll = l.strip()
        if ll == "":
            m = -1
            continue

        if ll.startswith("Monkey"):
            m = int(ll.replace("Monkey", "").replace(":", "").strip())
            d[m] = {}

        elif ll.startswith("Starting"):
            d[m]["items"] = [int(s.strip()) for s in ll.replace("Starting items:", "").split(",")]

        elif ll.startswith("Operation"):
            op = tuple(s.strip() for s in ll.replace("Operation: new = old", "").split())
            d[m]["op"] = op

        elif ll.startswith("Test"):
            d[m]["test"] = {}
            d[m]["test"]["div"] = int(ll.replace("Test: divisible by", "").strip())
        elif ll.startswith("If true:"):
            d[m]["test"]["true"] = int(ll.replace("If true: throw to monkey", "").strip())
        elif ll.startswith("If false:"):
            d[m]["test"]["false"] = int(ll.replace("If false: throw to monkey", "").strip())

    return d


def run_game(game, rounds: int, divisor_func: Callable[[int], int]):
    for _ in range(1, rounds + 1):
        for m in range(max(game) + 1):
            monkey = game[m]
            while monkey["items"]:
                item = monkey["items"].pop(0)
                monkey["inspections"] = monkey.get("inspections", 0) + 1
                op, val = monkey["op"]
                val = item if val == "old" else int(val)
                match op:
                    case "*":
                        item *= val
                    case "+":
                        item += val
                    case _:
                        raise RuntimeError("unknown op")

                item = divisor_func(item)
                if item % monkey["test"]["div"] == 0:
                    game[monkey["test"]["true"]]["items"].append(item)
                else:
                    game[monkey["test"]["false"]]["items"].append(item)

    result = np.prod(sorted([game[k]["inspections"] for k in game])[-2:])
    return result


def part_a(lines: List[str]) -> int:
    game = parse(lines)
    return run_game(game, 20, lambda x: x // 3)


def part_b(lines: List[str]) -> int:
    game = parse(lines)
    divisor = int(np.prod([2, 3, 5, 7, 11, 13, 17, 19, 23, 29]))
    return run_game(game, 10000, lambda x: x % divisor)


def run() -> None:
    print("partA:")
    print(part_a(read_input_to_list(__file__)))
    assert part_a(read_input_to_list(__file__)) == 100345
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 10605

    print("partB:")
    print(part_b(read_input_to_list(__file__)))
    assert part_b(read_input_to_list(__file__)) == 28537348205
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 2713310158

    print("done")
