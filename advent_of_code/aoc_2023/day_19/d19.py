from __future__ import annotations

import copy
import json
import re
from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np

from advent_of_code.commons.commons import read_input_to_list


@dataclass
class Rule:
    var_name: str
    value: int
    target: str
    op: str

    def apply(self, x_val):
        match self.op:
            case ">":
                return self.target if x_val > self.value else None
            case "<":
                return self.target if x_val < self.value else None
            case "default":
                return self.target
            case _:
                raise RuntimeError("Rule failure")


def parse(lines: List[str]) -> Tuple[Dict[str, List[Rule]], List[Dict]]:
    s_p = re.compile(r"([a-z])<([0-9]+):([a-z,A-Z]+)")
    g_p = re.compile(r"([a-z])>([0-9]+):([a-z,A-Z]+)")
    flows = {}
    parts = []
    do_parts = False
    for l in lines:
        if l == "":
            do_parts = True
            continue

        if do_parts:
            parts.append(
                json.loads(str(l.replace("=", ":").replace("{", '{"').replace(",", ',"').replace(":", '":')))
            )
        else:
            p = l.split("{")
            name = p[0].strip()
            p = p[1].replace("}", "").split(",")
            default = p[-1].strip()
            flows[name] = []
            for rule in p[:-1]:
                if m := s_p.match(rule.strip()):
                    mm = m.groups(0)
                    flows[name].append(Rule(var_name=mm[0], value=int(mm[1]), target=mm[2], op="<"))
                elif m := g_p.match(rule.strip()):
                    mm = m.groups(0)
                    flows[name].append(Rule(var_name=mm[0], value=int(mm[1]), target=mm[2], op=">"))
                else:
                    raise RuntimeError("No match found")

            flows[name].append(Rule(var_name="x", value=-1, target=default, op="default"))

    return flows, parts


def get_single_target_workflows(
    flows: Dict[str, List[Rule]], already_replaced: Dict[str, str]
) -> Dict[str, str]:
    d = {f: {r.target for r in flows[f]} for f in flows}
    d2 = {f: list(d[f])[0] for f in d if len(d[f]) == 1 and already_replaced.get(f) is None}
    return d2


def part_a(lines: List[str]) -> int:
    flows, parts = parse(lines)

    # optimize workflows
    already_replaced = {}
    single_target_flows = get_single_target_workflows(flows, already_replaced)
    while single_target_flows:
        for f in flows:
            for r in flows[f]:
                if single_target_flows.get(r.target):
                    r.target = single_target_flows[r.target]

        already_replaced.update(single_target_flows)
        single_target_flows = get_single_target_workflows(flows, already_replaced)

    # apply to parts
    accepted = []
    rejected = []
    for p in parts:
        pos = "in"
        while True:
            f = flows[pos]
            for r in f:
                if (new_pos := r.apply(p[r.var_name])) is not None:
                    pos = new_pos
                    break

            if pos == "A":
                accepted.append(p)
                break
            elif pos == "R":
                rejected.append(p)
                break

    s = sum([sum([p[k] for k in p]) for p in accepted])

    return s


def part_b(lines: List[str]) -> int:
    flows, parts = parse(lines)

    # optimize workflows
    already_replaced = {}
    single_target_flows = get_single_target_workflows(flows, already_replaced)
    while single_target_flows:
        for f in flows:
            for r in flows[f]:
                if single_target_flows.get(r.target):
                    r.target = single_target_flows[r.target]

        already_replaced.update(single_target_flows)
        single_target_flows = get_single_target_workflows(flows, already_replaced)

    #
    accepted = []
    to_refine = [{"f": "in", "x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)}]
    while to_refine:
        p = to_refine.pop()
        if p["f"] == "A":
            accepted.append(p)
            continue
        elif p["f"] == "R":
            continue

        f = flows[p["f"]]
        for r in f:
            v_min, v_max = p[r.var_name]
            if r.op == ">":
                if v_max > r.value:
                    new_p = copy.deepcopy(p)
                    new_p["f"] = r.target
                    new_p[r.var_name] = (r.value + 1, v_max)
                    to_refine.append(new_p)

                p[r.var_name] = (v_min, r.value)
            elif r.op == "<":
                if v_min < r.value:
                    new_p = copy.deepcopy(p)
                    new_p["f"] = r.target
                    new_p[r.var_name] = (v_min, r.value - 1)
                    to_refine.append(new_p)

                p[r.var_name] = (r.value, v_max)
            else:
                p["f"] = r.target
                to_refine.append(p)

    s = 0
    for p in accepted:
        m = 1
        for k in p:
            if k != "f":
                m *= p[k][1] - p[k][0] + 1
        s += m

    return s


def run() -> None:
    print("partA:")
    assert part_a(read_input_to_list(__file__)) == 575412
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 19114

    print("partB:")
    assert part_b(read_input_to_list(__file__)) == 126107942006821
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 167409079868000
    print("done")
