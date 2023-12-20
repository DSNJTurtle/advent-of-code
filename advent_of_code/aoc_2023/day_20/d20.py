"""No clean code solution today ;)"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Tuple

from advent_of_code.commons.commons import read_input_to_list

Pulse = int


def parse(lines: List[str]):
    d = {"ff": {}, "conv": {}}
    for l in lines:
        parts = l.split("->")
        if l.startswith("broadcaster"):
            d["bc"] = tuple([s.strip() for s in parts[1].strip().split(",")])
        elif l.startswith("%"):
            f = parts[0].lstrip("%").strip()
            t = tuple([s.strip() for s in parts[1].strip().split(",")])
            d["ff"].update({f: t})
        elif l.startswith("&"):
            f = parts[0].lstrip("&").strip()
            t = tuple([s.strip() for s in parts[1].strip().split(",")])
            d["conv"].update({f: t})
        else:
            raise RuntimeError("unknown content")

    return d


class State:
    def __init__(self, bc: Tuple[str], ff: Dict[str, Tuple[str]], conv: Dict[str, Tuple[str]]):
        self.n_low_pulses = 0
        self.n_high_pulses = 0
        self.bc = bc
        self.ff = ff
        self.conv = conv

        all_nodes = set(bc)
        for k in ff:
            all_nodes.add(k)
            for kk in ff[k]:
                all_nodes.add(kk)
        for k in conv:
            all_nodes.add(k)
            for kk in conv[k]:
                all_nodes.add(kk)

        self.outputs = [o for o in all_nodes if o not in ff and o not in conv and o not in bc]
        self.all_node_map = {n: i for i, n in enumerate(sorted(all_nodes))}

        # all high inputs for conv registers
        self.conv_all_high = {}
        for c in self.conv:
            inputs = set()
            for x in [k for k in self.ff if c in self.ff[k]]:
                inputs.add(x)
            for x in [k for k in self.conv if c in self.conv[k]]:
                inputs.add(x)
            # broadcast is not input to conv

            self.conv_all_high[c] = int(sum([self.bitmask(t) for t in inputs]))

        # states
        self.ff_map = {n: i for i, n in enumerate(sorted(self.ff))}
        self.ff_state = [0] * len(self.ff_map)

        self.conv_map = {n: i for i, n in enumerate(sorted(self.conv))}
        self.conv_state = [0] * len(self.conv_map)  # state of inputs to conv node

    def add_pulse(self, p: Pulse) -> None:
        if p == 0:
            self.n_low_pulses += 1
        else:
            self.n_high_pulses += 1

    def flip(self, target) -> Pulse:
        idx = self.ff_map[target]
        self.ff_state[idx] = (self.ff_state[idx] + 1) % 2
        if self.ff_state[idx] == 1:
            return 1
        else:
            return 0

    def conv(self, target, source, p: Pulse) -> Pulse:
        idx = self.conv_map[target]
        if p == 0:
            self.conv_state[idx] &= ~self.bitmask(source)
        else:
            self.conv_state[idx] |= self.bitmask(source)

        if self.conv_state[idx] == self.conv_all_high[target]:
            return 0
        else:
            return 1

    def bitmask(self, target) -> int:
        return pow(2, self.all_node_map[target])

    def get_cache(self):
        return tuple(self.ff_state), tuple(self.conv_state)


@dataclass(frozen=True)
class CacheState:
    n_pushes: int
    n_low_pulses: int
    n_high_pulses: int


def part_a(lines: List[str]) -> int:
    setup = parse(lines)
    state = State(setup["bc"], setup["ff"], setup["conv"])
    # cache = {}
    do_print = False
    target_pushes = 1000

    to_send = []
    n_pushes = 0
    while True:
        n_pushes += 1
        to_send.append(("button", "bc", 0))
        if do_print:
            print("button -low-> bc")

        while to_send:
            source, target, pulse = to_send.pop(0)
            state.add_pulse(pulse)
            if target == "bc":
                for t in setup["bc"]:
                    if do_print:
                        print(f"bc -{'low' if pulse == 0 else 'high'}-> {t}")
                    to_send.append(("bc", t, pulse))
            elif target in state.ff_map:
                if pulse == 0:
                    new_pulse = state.flip(target)
                    for t in state.ff[target]:
                        if do_print:
                            print(f"{target} -{'low' if new_pulse == 0 else 'high'}-> {t}")
                        to_send.append((target, t, new_pulse))
            elif target in state.conv_map:
                new_pulse = state.conv(target, source, pulse)
                for t in state.conv[target]:
                    if do_print:
                        print(f"{target} -{'low' if new_pulse == 0 else 'high'}-> {t}")
                    to_send.append((target, t, new_pulse))
            elif target in state.outputs:
                # print(f"reached output {target}")
                pass
            else:
                raise RuntimeError("unknown target")

        # if cache is not None:
        #     new_hash = state.get_cache()
        #     if new_hash in cache:
        #         old_state = cache[new_hash]
        #         new_state = CacheState(n_pushes, state.n_low_pulses, state.n_high_pulses)
        #         period = new_state.n_pushes - old_state.n_pushes
        #         q, r = divmod(target_pushes - n_pushes, period)
        #         n_pushes = target_pushes - r
        #         state.n_low_pulses += (new_state.n_low_pulses - old_state.n_low_pulses) * q
        #         state.n_high_pulses += (new_state.n_high_pulses - old_state.n_high_pulses) * q
        #         cache = None  # stop tracking when we found a period
        #     else:
        #         cache[new_hash] = CacheState(n_pushes, state.n_low_pulses, state.n_high_pulses)

        if n_pushes == target_pushes:
            break

        if do_print:
            print("\n")

    return state.n_low_pulses * state.n_high_pulses


def part_b(lines: List[str]) -> int:
    setup = parse(lines)
    state = State(setup["bc"], setup["ff"], setup["conv"])
    do_print = False

    to_send = []
    n_pushes = 0
    # 0 to rx, iff output of &dn == 0
    # All inputs to &dn == 1 --> All outputs from {&dd,&fh,&xp,&fc} must be 1
    min_cycle_lengths = {"dd": -1, "fh": -1, "xp": -1, "fc": -1}
    while True:
        n_pushes += 1
        to_send.append(("button", "bc", 0))
        if do_print:
            print("button -low-> bc")

        while to_send:
            source, target, pulse = to_send.pop(0)
            state.add_pulse(pulse)
            if target == "bc":
                for t in setup["bc"]:
                    if do_print:
                        print(f"bc -{'low' if pulse == 0 else 'high'}-> {t}")
                    to_send.append(("bc", t, pulse))
            elif target in state.ff_map:
                if pulse == 0:
                    new_pulse = state.flip(target)
                    for t in state.ff[target]:
                        if do_print:
                            print(f"{target} -{'low' if new_pulse == 0 else 'high'}-> {t}")
                        to_send.append((target, t, new_pulse))
            elif target in state.conv_map:
                new_pulse = state.conv(target, source, pulse)
                for t in state.conv[target]:
                    if do_print:
                        print(f"{target} -{'low' if new_pulse == 0 else 'high'}-> {t}")
                    to_send.append((target, t, new_pulse))
                    if (v := min_cycle_lengths.get(target)) and v == -1 and new_pulse == 1:
                        min_cycle_lengths[target] = n_pushes
            elif target in state.outputs:
                if pulse == 0:
                    return n_pushes
            else:
                raise RuntimeError("unknown target")

        if all([min_cycle_lengths[k] > 0 for k in min_cycle_lengths]):
            break

    res = math.lcm(*[min_cycle_lengths[k] for k in min_cycle_lengths])
    return res


def run() -> None:
    print("partA:")
    print(part_a(read_input_to_list(__file__)))
    assert part_a(read_input_to_list(__file__)) == 899848294
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 11687500
    assert part_a(read_input_to_list(__file__, filename="test1.txt", read_test_input=True)) == 32000000

    print("partB:")
    print(part_b(read_input_to_list(__file__)))
    assert part_b(read_input_to_list(__file__)) == 247454898168563

    print("done")
