from __future__ import annotations

from typing import Dict, List

import networkx as nx

from advent_of_code.commons.commons import read_input_to_list


def parse_grid(lines: List[str]):
    grid = {complex(i, j): c for i, r in enumerate(lines) for j, c in enumerate(r)}
    return grid


def build_reduced_graph(grid: Dict[complex, str]):
    g = nx.DiGraph()
    allowed_steps = {">": {1j}, "<": {-1j}, "v": {1}, "^": {-1}}

    for pos, c in grid.items():
        if c == "#":
            continue

        for step in allowed_steps.get(grid[pos], {1, -1, 1j, -1j}):
            new_pos = pos + step
            if (new_c := grid.get(new_pos)) and new_c != "#":
                rev_step = allowed_steps.get(new_c)
                if rev_step is None or rev_step != -step:
                    g.add_edge(pos, new_pos, weight=1)

    # prune 2-connectivity nodes
    nodes_to_remove = []
    for n in g.nodes:
        a = tuple(g.adj[n])
        if len(a) == 2:
            s, e = a
            if g.has_edge(s, n) and g.has_edge(n, e):
                w = g[s][n]["weight"] + g[n][e]["weight"]
                g.add_edge(s, e, weight=w)
                g.remove_edge(s, n)
                g.remove_edge(n, e)

            if g.has_edge(e, n) and g.has_edge(n, s):
                w = g[n][s]["weight"] + g[e][n]["weight"]
                g.add_edge(e, s, weight=w)
                g.remove_edge(e, n)
                g.remove_edge(n, s)

            if g.degree(n) == 0:
                nodes_to_remove.append(n)

    for n in nodes_to_remove:
        g.remove_node(n)

    return g


def part_a(lines: List[str]) -> int:
    grid = parse_grid(lines)
    n_rows = int(max(p.real for p in grid))
    n_cols = int(max(p.imag for p in grid))
    start_pos = complex(0, 1)
    end_pos = complex(n_rows, n_cols - 1)
    g = build_reduced_graph(grid)
    n_steps = max(nx.path_weight(g, p, weight="weight") for p in nx.all_simple_paths(g, start_pos, end_pos))

    return n_steps


def part_b(lines: List[str]) -> int:
    grid = parse_grid(lines)
    for i, c in grid.items():
        if c in (">", "<", "v", "^"):
            grid[i] = "."
    n_rows = int(max(p.real for p in grid))
    n_cols = int(max(p.imag for p in grid))
    start_pos = complex(0, 1)
    end_pos = complex(n_rows, n_cols - 1)
    g = build_reduced_graph(grid)
    g = g.to_undirected()
    n_steps = max(nx.path_weight(g, p, weight="weight") for p in nx.all_simple_paths(g, start_pos, end_pos))

    return n_steps


def run() -> None:
    print("partA:")
    res = part_a(read_input_to_list(__file__))
    print(res)
    assert res == 2194
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 94

    print("partB:")
    res = part_b(read_input_to_list(__file__))
    print(res)
    assert res == 6410
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 154

    print("done")
