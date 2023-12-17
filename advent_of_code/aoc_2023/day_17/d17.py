from __future__ import annotations

from typing import Dict, List

import networkx as nx
import numpy as np
from networkx import astar_path
from tqdm import tqdm

from advent_of_code.commons.commons import read_input_to_list


def parse_dict(lines: List[str]):
    return {complex(i, j): int(c) for i, r in enumerate(lines) for j, c in enumerate(r)}


def build_graph(d: Dict, max_path_length: int, skip_n_first: int = None):
    g = nx.DiGraph()
    for n in d:
        for incoming_dir in [1j, 1, -1, -1j]:
            current_node = n
            # build forward graph
            for path_length in range(max_path_length - 1):
                next_node = current_node + incoming_dir
                if next_node_w := d.get(next_node):
                    g.add_edge(
                        (current_node, incoming_dir, path_length),
                        (next_node, incoming_dir, path_length + 1),
                        weight=next_node_w,
                    )
                    current_node = next_node
                else:
                    break

            current_node = n
            # build orthogonal nodes along forward path
            for path_length in range(max_path_length):
                if skip_n_first is not None and path_length < skip_n_first:
                    # skip first n nodes (part b)
                    next_node = current_node + incoming_dir
                    if d.get(next_node):
                        current_node = next_node
                        continue
                    else:
                        break

                o_dir = complex(incoming_dir.imag, incoming_dir.real)
                for o_dir in [o_dir, -o_dir]:
                    next_node = current_node + o_dir
                    if next_node_w := d.get(next_node):
                        g.add_edge(
                            (current_node, incoming_dir, path_length),
                            (next_node, o_dir, 0),
                            weight=next_node_w,
                        )

                next_node = current_node + incoming_dir
                if d.get(next_node):
                    current_node = next_node
                else:
                    break

    return g


def manhatten(a, b) -> float:
    return abs(a[0] - b[0])


class PrintGrid:
    def __init__(self, grid, initial="."):
        self.initial = initial
        n_rows = int(max(k.real for k in grid)) + 1
        n_cols = int(max(k.imag for k in grid)) + 1
        self.grid = np.zeros((n_rows, n_cols), dtype=int)

    def show(self):
        print()
        for g in self.grid:
            print(" ".join([str(i) for i in g]).replace("0", self.initial))

        print()
        print()

    def update(self, entries: List[complex]) -> None:
        for e in entries:
            re, im = e.real, e.imag
            if 0 <= re < len(self.grid) and 0 <= im < len(self.grid[0]):
                self.grid[int(e.real)][int(e.imag)] += 1


def get_shortest_path(d, g, source_nodes, target_nodes):
    paths = []
    configs = [(s, t) for s in source_nodes for t in target_nodes]
    for s, t in tqdm(configs):
        try:
            # no gain using A* here. Dijkstra works too
            paths.append(astar_path(g, s, t, weight="weight", heuristic=manhatten))
        except Exception as _:
            pass

    # for p in paths:
    #     pgrid = PrintGrid(d)
    #     pgrid.update([x for x, _, _ in p])
    #     pgrid.show()

    weights_per_path = [
        [d.get(pos) for pos, _, _ in p[1:]] for p in paths
    ]  # drop entry point weight from path
    weights = [sum(x) for x in weights_per_path]
    min_w = min(weights)

    return min_w


def part_a(lines: List[str]) -> int:
    d = parse_dict(lines)
    g = build_graph(d, 3)
    source_nodes = [(0j, i, 0) for i in [1, 1j]]
    target_pos = complex(len(lines) - 1, len(lines[0]) - 1)
    target_nodes = list(filter(lambda x: x[0] == target_pos and x[1] in [1, 1j], g.nodes))
    min_w = get_shortest_path(d, g, source_nodes, target_nodes)

    return min_w


def part_b(lines: List[str]) -> int:
    d = parse_dict(lines)
    g = build_graph(d, 10, 3)
    source_nodes = [(0j, i, 0) for i in [1, 1j]]
    target_pos = complex(len(lines) - 1, len(lines[0]) - 1)
    target_nodes = list(filter(lambda x: x[0] == target_pos and x[1] in [1, 1j] and x[2] >= 3, g.nodes))
    min_w = get_shortest_path(d, g, source_nodes, target_nodes)

    return min_w


def run() -> None:
    print("partA:")
    assert part_a(read_input_to_list(__file__)) == 797
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 102

    print("partB:")
    assert part_b(read_input_to_list(__file__)) == 914
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 94
    assert part_b(read_input_to_list(__file__, filename="test2.txt", read_test_input=True)) == 71

    print("done")
