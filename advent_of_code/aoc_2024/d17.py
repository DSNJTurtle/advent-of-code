import math
import re

from advent_of_code.commons.commons import read_input_to_list


def combo_operand(operand: int, registers: dict[str, int]) -> int:
    if operand in (0, 1, 2, 3):
        return operand
    elif operand == 4:
        return registers["A"]
    elif operand == 5:
        return registers["B"]
    elif operand == 6:
        return registers["C"]
    else:
        raise ValueError("Invalid operand")


def part_a(lines: list[str]) -> str:
    p1 = re.compile(r"Register (\w+): (\d+)")
    registers = {}
    program = None
    for line in lines:
        m1 = p1.match(line)
        if m1:
            reg, val = m1.groups()
            registers[reg] = int(val)
        elif line.startswith("Program"):
            program = [int(x) for x in line.replace("Program:", "").strip().split(",")]

    output = []
    pointer = 0
    while pointer < len(program) - 1:
        opcode = program[pointer]
        operand = program[pointer + 1]

        if opcode == 0:
            registers["A"] = registers["A"] // int(math.pow(2, combo_operand(operand, registers)))
        elif opcode == 1:
            registers["B"] = registers["B"] ^ operand
        elif opcode == 2:
            registers["B"] = int(combo_operand(operand, registers) % 8)
        elif opcode == 3:
            if registers["A"] == 0:
                pass
            else:
                pointer = operand
                continue
        elif opcode == 4:
            registers["B"] = registers["B"] ^ registers["C"]
        elif opcode == 5:
            # out
            output.append(int(combo_operand(operand, registers) % 8))
        elif opcode == 6:
            registers["B"] = registers["A"] // int(math.pow(2, combo_operand(operand, registers)))
        elif opcode == 7:
            registers["C"] = registers["A"] // int(math.pow(2, combo_operand(operand, registers)))

        pointer += 2

    return ",".join([str(x) for x in output])


def part_b(lines: list[str]) -> int:
    p1 = re.compile(r"Register (\w+): (\d+)")
    registers = {}
    program = None
    for line in lines:
        m1 = p1.match(line)
        if m1:
            reg, val = m1.groups()
            registers[reg] = int(val)
        elif line.startswith("Program"):
            program = [int(x) for x in line.replace("Program:", "").strip().split(",")]

    # a = 23400000
    a = 0
    # cycle_length = 0
    while True:
        if a % 100_000 == 0:
            print(f"Trying a={a}")
        registers["A"] = a
        registers["B"] = 0
        registers["C"] = 0
        output = []
        pointer = 0
        while pointer < len(program) - 1:
            opcode = program[pointer]
            operand = program[pointer + 1]
            # cycle_length += 1

            # if pointer == 0:
            #     print(f"Trying a={a}")
            #     print(f"cycle_length: {cycle_length}")
            #     print(f"Registers: {registers}")
            #     print(f"Program: {program}")
            #     print(f"Output: {output}")
            #     print()
            #     cycle_length = 0

            if opcode == 0:
                registers["A"] = registers["A"] // int(math.pow(2, combo_operand(operand, registers)))
            elif opcode == 1:
                registers["B"] = registers["B"] ^ operand
            elif opcode == 2:
                registers["B"] = int(combo_operand(operand, registers) % 8)
            elif opcode == 3:
                if registers["A"] == 0:
                    pass
                else:
                    pointer = operand
                    continue
            elif opcode == 4:
                registers["B"] = registers["B"] ^ registers["C"]
            elif opcode == 5:
                # out
                output.append(int(combo_operand(operand, registers) % 8))
            elif opcode == 6:
                registers["B"] = registers["A"] // int(math.pow(2, combo_operand(operand, registers)))
            elif opcode == 7:
                registers["C"] = registers["A"] // int(math.pow(2, combo_operand(operand, registers)))

            pointer += 2

        if output == program:
            break

        # a += 1
        a += 9

    return a


def run() -> None:
    print("partA:")
    res = part_a(read_input_to_list(__file__))
    print(res)
    assert res == "2,1,3,0,5,2,3,7,1"
    # assert part_a(read_input_to_list(__file__, read_test_input=True)) == "4,6,3,5,6,3,5,2,1,0"

    print("partB:")
    res = part_b(read_input_to_list(__file__))
    print(res)
    # assert res == 551
    # assert part_b(read_input_to_list(__file__, read_test_input=True)) == 117440

    print("done")
