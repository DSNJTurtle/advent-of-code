import math
import sys
from typing import Dict, List

from aoc_2023.commons.commons import read_input_to_list


class CircularList:
    def __init__(self, instructions, start_pos=0):
        self.instructions = instructions
        self.length = len(instructions)
        assert self.length > 0
        self.pos = start_pos - 1

    def next_instruction(self) -> str:
        self.set_pos(self.pos + 1)
        return self.instructions[self.pos]

    def set_pos(self, pos: int) -> None:
        self.pos = pos % self.length


def parse(lines: List[str]):
    instructions = [s for s in lines[0].strip()]

    d = {}
    for l in lines[2:]:
        parts = l.split("=")
        source = parts[0].strip()
        targets = parts[1].strip().replace("(", "").replace(")", "").split(",")
        d.update({source: {"L": targets[0].strip(), "R": targets[1].strip()}})

    return instructions, d


def part_a(lines: List[str]) -> int:
    instructions, network = parse(lines)
    instructions = CircularList(instructions)

    curr_node = "AAA"
    n_steps = 0
    while curr_node != "ZZZ":
        n_steps += 1
        next_nodes = network[curr_node]
        curr_node = next_nodes[instructions.next_instruction()]

    return n_steps


def n_steps_until_end(instructions: CircularList, network: Dict, start_node: str):
    curr_node = start_node
    n_steps = 0
    while True:
        n_steps += 1
        next_nodes = network[curr_node]
        n = next_nodes[instructions.next_instruction()]
        if curr_node == n:
            # circular deps
            return sys.maxsize, start_node

        curr_node = n

        if curr_node.endswith("Z"):
            break

    return n_steps, curr_node


def part_b(lines: List[str]) -> int:
    """
    Luckily the input hits the "Z" endpoints every cycle length. Hence, use lcm.
    Does not work in a more general case.
    """
    instructions, network = parse(lines)
    instructions = CircularList(instructions)
    curr_nodes = [s for s in network.keys() if s.endswith("A")]
    n_steps = [n_steps_until_end(instructions, network, s)[0] for s in curr_nodes]

    lcm = math.lcm(*n_steps)
    return lcm


def run() -> None:
    print("partA:")
    assert part_a(read_input_to_list(__file__)) == 16579
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 2
    assert part_a(read_input_to_list(__file__, filename="test2.txt", read_test_input=True)) == 6

    print("partB:")
    assert part_b(read_input_to_list(__file__)) == 12927600769609
    assert part_b(read_input_to_list(__file__, filename="testB.txt", read_test_input=True)) == 6

    print("done")
