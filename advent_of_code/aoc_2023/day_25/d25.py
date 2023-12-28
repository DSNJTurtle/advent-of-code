from __future__ import annotations

from typing import List

import networkx as nx
import numpy as np

from advent_of_code.commons.commons import read_input_to_list


def parse_graph(lines: List[str]):
    g = nx.Graph()
    for l in lines:
        parts = l.split(":")
        p0 = parts[0].strip()
        for p in parts[1].split():
            pp = p.strip()
            g.add_edge(p0, pp, weight=1)

    return g


def part_a(lines: List[str]) -> int:
    g = parse_graph(lines)
    edges_to_cut = nx.minimum_edge_cut(g)
    for a, b in edges_to_cut:
        g.remove_edge(a, b)

    res = [n for n in nx.connected_components(g)]
    res = int(np.prod([len(s) for s in res]))
    return res


def part_b(lines: List[str]) -> int:
    pass


def run() -> None:
    print("partA:")
    res = part_a(read_input_to_list(__file__))
    print(res)
    assert res == 598120
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 54

    print("partB:")
    # res = part_b(read_input_to_list(__file__))
    # print(res)
    # assert res == 848947587263033
    # assert part_b(read_input_to_list(__file__, read_test_input=True)) == 47

    print("done")
