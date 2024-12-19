from advent_of_code.commons.commons import read_input_to_list


def parse(lines: list[str]):
    grid = {complex(i, j): str(s) for i, line in enumerate(lines) for j, s in enumerate(line)}

    start_pos = 0
    for key, value in grid.items():
        if value == "^":
            start_pos = key

    return grid, start_pos


def part_a(lines: list[str]) -> int:
    grid, position = parse(lines)
    max_row = len(lines) - 1
    max_col = len(lines[0]) - 1

    update = -1
    visited = {position}

    while update is not None:
        new_position = position + update
        if (0 <= new_position.real <= max_row) and (0 <= new_position.imag <= max_col):
            g = grid[new_position]
            if g == "#":
                update *= complex(0, -1)
            else:
                visited.add(new_position)
                position = new_position
        else:
            update = None

    return len(visited)


def part_b(lines: list[str]) -> int:
    grid, start_position = parse(lines)
    grid[start_position] = "|"

    max_row = len(lines) - 1
    max_col = len(lines[0]) - 1

    n_loops = 0
    counter = 0
    for r in range(max_row + 1):
        for c in range(max_col + 1):
            counter += 1
            if counter % 1000 == 0:
                print(f"Iter {counter} / {(max_row + 1) * (max_col + 1)}")
            obstacle_pos = complex(r, c)
            prev_obstacle = grid[obstacle_pos]
            if obstacle_pos != start_position:
                # update grid
                new_grid = grid
                new_grid[obstacle_pos] = "#"
                update = complex(-1, 0)
                # track tuples of visited positions and orientations at that position (position, orientation)
                positions = {(start_position, update)}
                position = start_position
                while True:
                    new_position = position + update
                    if (0 <= new_position.real <= max_row) and (0 <= new_position.imag <= max_col):
                        g = new_grid[new_position]
                        if (new_position, update) in positions:
                            # found loop
                            n_loops += 1
                            break
                        elif g == "#":
                            # update orientation
                            update *= complex(0, -1)
                            positions.add((position, update))
                        else:
                            # position update
                            position = new_position
                            positions.add((position, update))
                    else:
                        # guard leaves grid
                        break

                # revert grid update (slightly faster than making a copy)
                grid[obstacle_pos] = prev_obstacle

    return n_loops


def run() -> None:
    print("partA:")
    res = part_a(read_input_to_list(__file__))
    print(res)
    assert res == 5564
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 41

    print("partB:")
    res = part_b(read_input_to_list(__file__))
    print(res)
    assert res == 1976
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 6

    print("done")
