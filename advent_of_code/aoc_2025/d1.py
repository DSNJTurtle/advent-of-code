from aocd.models import Puzzle, User


def part_a(input_data: str) -> str:
    data = [x.replace("L", "-").replace("R", "") for x in input_data.strip().split("\n")]
    data = [int(x) for x in data]

    pos = 50
    c = 0
    for p in data:
        pos += p
        if pos < 0:
            pos += 100

        pos = pos % 100

        if pos == 0:
            c += 1

    return str(c)


def part_b(input_data: str) -> str:
    data = [x.replace("L", "-").replace("R", "") for x in input_data.strip().split("\n")]
    data = [int(x) for x in data]

    pos = 50
    c = 0
    for p in data:
        old_pos = pos
        pos += p
        if p < 0:
            if pos < 0:
                c += abs(pos) // 100
                if old_pos != 0:
                    c += 1
                pos = pos % 100
            elif pos == 0:
                c += 1
        elif p == 0:
            print("got zero. what should we do?")
            c += 1
        else:
            c += pos // 100  # this counts when hitting zero
            pos = pos % 100

    return str(c)


if __name__ == "__main__":
    token = ""
    p = Puzzle(2025, 1, user=User(token=token))

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
