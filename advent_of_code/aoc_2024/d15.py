from numbers import Complex

from advent_of_code.commons.commons import read_input_to_list


def parse_a(lines: list[str]) -> tuple[Complex, dict[Complex, str], list[Complex]]:
    # find end of grid
    split_line = 0
    for i in range(len(lines)):
        if lines[i] == "":
            split_line = i
            break

    grid = lines[:split_line]
    moves = lines[split_line + 1 :]

    # parse grid
    grid = {i + j * 1j: c for i, line in enumerate(grid) for j, c in enumerate(line)}

    start_pos = 0
    for k, v in grid.items():
        if v == "@":
            start_pos = k
            break

    # parse moves
    _map = {"<": -1j, ">": 1j, "^": -1 + 0j, "v": 1 + 0j}
    m = [_map[c] for c in "".join(moves)]

    return start_pos, grid, m


def parse_b(lines: list[str]) -> tuple[Complex, dict[Complex, str], list[Complex]]:
    # find end of grid
    split_line = 0
    for i in range(len(lines)):
        if lines[i] == "":
            split_line = i
            break

    grid_lines = lines[:split_line]
    moves = lines[split_line + 1 :]

    # parse grid
    grid = {}
    i = 0
    while len(grid_lines) > 0:
        line = list(grid_lines.pop(0))
        j = 0
        while len(line) > 0:
            c = line.pop(0)
            if c == "#":
                grid[i + j * 1j] = "#"
                j += 1
                grid[i + j * 1j] = "#"
            elif c == "O":
                grid[i + j * 1j] = "["
                j += 1
                grid[i + j * 1j] = "]"
            elif c == ".":
                grid[i + j * 1j] = "."
                j += 1
                grid[i + j * 1j] = "."
            elif c == "@":
                grid[i + j * 1j] = "@"
                j += 1
                grid[i + j * 1j] = "."
            j += 1
        i += 1

    start_pos = 0
    for k, v in grid.items():
        if v == "@":
            start_pos = k
            break

    # parse moves
    _map = {"<": -1j, ">": 1j, "^": -1 + 0j, "v": 1 + 0j}
    m = [_map[c] for c in "".join(moves)]

    return start_pos, grid, m


def visualize(grid: dict[Complex, str], grid_max: tuple[int, int]) -> None:
    m, n = grid_max
    for x in range(m + 1):
        s = "".join([grid.get(x + y * 1j, ".") for y in range(n + 1)])
        print(s)
    print()


def score_a(grid: dict[Complex, str], char: str) -> int:
    positions = [k for k, v in grid.items() if v == char]
    scores = [p.real * 100 + p.imag for p in positions]
    return int(sum(scores))


def solve(lines: list[str], is_part_b: bool) -> int:
    pos, grid, moves = parse_a(lines) if not is_part_b else parse_b(lines)
    # sx = int(max([p.real for p in grid.keys()]))
    # sy = int(max([p.imag for p in grid.keys()]))

    for m in moves:
        # visualize(grid, (sx, sy))
        # print(f"move: {m}")

        # create a list of positions to update for each move
        to_update = [pos]
        i = 0  # lags behind to_update
        is_impossible = False  # if we hit a wall
        # bfs to find all positions to update
        while i < len(to_update):
            c = to_update[i]
            new_c = c + m
            # do we need to iterate?
            if grid[new_c] in "O[]":
                if new_c not in to_update:  # checks only to remove duplicates in part b
                    # "O" case or part of box
                    to_update.append(new_c)
                if grid[new_c] == "[":
                    # also add rhs of box
                    new_c2 = new_c + 1j
                    if new_c2 not in to_update:
                        to_update.append(new_c2)
                if grid[new_c] == "]":
                    # also add lhs of box
                    new_c2 = new_c - 1j
                    if new_c2 not in to_update:
                        to_update.append(new_c2)
            elif grid[new_c] == "#":
                is_impossible = True
                break
            i += 1

        if is_impossible:
            # discard update list and continue
            continue

        # use new grid as buffer
        new_grid = {k: v for k, v in grid.items()}
        to_update.reverse()  # ensure to move last box first
        for c in to_update:
            new_grid[c + m] = grid[c]
            new_grid[c] = "."

        grid = new_grid
        pos += m

    # visualize(grid, (sx, sy))
    s = score_a(grid, char="[" if is_part_b else "O")
    return s


def run() -> None:
    print("partA:")
    res = solve(read_input_to_list(__file__), is_part_b=False)
    print(res)
    assert res == 1497888
    # assert part_a2(read_input_to_list(__file__, read_test_input=True), is_part_b=False) == 2028  # smaller example
    assert solve(read_input_to_list(__file__, read_test_input=True), is_part_b=False) == 10092  # larger example

    print("partB:")
    res = solve(read_input_to_list(__file__), is_part_b=True)
    print(res)
    assert res == 1522420
    assert solve(read_input_to_list(__file__, read_test_input=True), is_part_b=True) == 9021

    print("done")
