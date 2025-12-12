import functools

import networkx as nx
from aocd.models import Puzzle, User


def part_a(input_data: str) -> str:
    nodes = []
    for line in input_data.splitlines():
        node, outputs = line.split(":", 1)
        nodes.append((node.strip(), [o.strip() for o in outputs.split()]))

    edges = []
    for k, v in nodes:
        for vv in v:
            edges.append((k, vv))

    network = nx.DiGraph(edges)
    paths = list(nx.all_simple_paths(network, "you", "out"))

    return str(len(paths))


def part_b(input_data: str) -> str:
    # this very nice answer was taken from https://www.reddit.com/user/willsowerbutts/
    # but only works if there are no loops, or if we are lucky
    nodes = {}
    for line in input_data.splitlines():
        node, outputs = line.split(":", 1)
        nodes[node.strip()] = [o.strip() for o in outputs.split()]

    @functools.cache  # FTW
    def count_routes(current_node, visited_dac, visited_fft):
        match current_node:
            case "out":
                return 1 if (visited_dac and visited_fft) else 0
            case "dac":
                visited_dac = True
            case "fft":
                visited_fft = True
        return sum(count_routes(node, visited_dac, visited_fft) for node in nodes[current_node])

    return str(count_routes("svr", False, False))


if __name__ == "__main__":
    token = ""
    p = Puzzle(2025, 11, user=User(token=token))

    if True:
        r = part_a(p.examples[0].input_data)
        print(f"Part A - Example Answer: {r}")
        assert r == "5"
        r = part_a(p.input_data)
        print(f"Part A - Answer: {r}")
        p.answer_a = r

    if True:
        # r = part_b(p.examples[0].input_data)
        # print(f"Part B - Example Answer: {r}")
        # assert r == "2"
        r = part_b(p.input_data)
        print(f"Part B - Answer: {r}")
        p.answer_b = r
