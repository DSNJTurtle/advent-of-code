from aocd.models import Puzzle, User


def part_a(input_data: str) -> str:
    data = [[int(y) for y in x.split("-")] for x in input_data.split(",")]

    invalid = []
    for a, b in data:
        for n in range(a, b + 1):
            s = str(n)
            ls = len(s)
            if ls % 2 == 0:
                s1 = s[: ls // 2]
                s2 = s[ls // 2 :]
                if s1 == s2:
                    invalid.append(n)

    return str(sum(invalid))


def part_b(input_data: str) -> str:
    data = [[int(y) for y in x.split("-")] for x in input_data.split(",")]

    invalid = []
    for a, b in data:
        for n in range(a, b + 1):
            s = str(n)
            ls = len(s)

            divisor = 2
            while divisor <= ls:
                r = split_n_parts_equal(s, divisor)
                if r:
                    invalid.append(n)
                    break

                divisor += 1

    return str(sum(invalid))


def split_n_parts_equal(s: str, n: int) -> bool:
    if len(s) % n != 0:
        return False

    ls = len(s)
    ls_part = ls // n
    first_part = s[0:ls_part]
    return all(s[i * ls_part : (i + 1) * ls_part] == first_part for i in range(1, n))


if __name__ == "__main__":
    token = ""
    p = Puzzle(2025, 2, user=User(token=token))

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
