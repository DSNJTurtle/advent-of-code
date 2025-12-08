from dataclasses import dataclass

from aocd.models import Puzzle, User


@dataclass
class Range:
    """Range."""

    lb: int
    rb: int

    @staticmethod
    def from_str(s: str) -> "Range":
        p = s.split("-")
        lb = int(p[0])
        rb = int(p[1])

        return Range(lb, rb)

    def is_fresh(self, _id: int) -> bool:
        return self.lb <= _id <= self.rb


def part_a(input_data: str) -> str:
    data = input_data.splitlines()
    ranges = [Range.from_str(x) for x in data if "-" in x]
    ids = [x for x in data if "-" not in x][1:]
    ids = [int(x) for x in ids]

    fresh_ids = [x for x in ids if is_fresh(x, ranges)]

    return str(len(fresh_ids))


def is_fresh(_id: int, ranges: list[Range]) -> bool:
    return any(r.is_fresh(_id) for r in ranges)


def part_b(input_data: str) -> str:
    data = input_data.splitlines()
    ranges = sorted([Range.from_str(x) for x in data if "-" in x], key=lambda r: r.lb)

    finished = []
    current = ranges[0]
    remaining = ranges[1:]

    while remaining:
        nr = remaining.pop(0)

        if nr.is_fresh(current.lb) and nr.is_fresh(current.rb):
            # current is in next
            current = nr
            continue

        if current.is_fresh(nr.lb) and current.is_fresh(nr.rb):
            # next is in current
            continue

        if not current.is_fresh(nr.lb):
            # no overlap
            finished.append(current)
            current = nr
            continue

        if current.is_fresh(nr.lb):
            current.rb = nr.rb
            continue

    finished.append(current)

    remaining_ranges = finished
    n_ids = [r.rb - r.lb + 1 for r in remaining_ranges]

    return str(sum(n_ids))


if __name__ == "__main__":
    token = ""
    p = Puzzle(2025, 5, user=User(token=token))

    if True:
        r = part_a(p.examples[0].input_data)
        print(f"Part A - Example Answer: {r}")
        assert r == p.examples[0].answer_a
        r = part_a(p.input_data)
        print(f"Part A - Answer: {r}")
        p.answer_a = r

    if True:
        r = part_b(p.examples[0].input_data)
        print(f"Part B - Example Answer: {r}")
        assert r == p.examples[0].answer_b
        r = part_b(p.input_data)
        print(f"Part B - Answer: {r}")
        p.answer_b = r
