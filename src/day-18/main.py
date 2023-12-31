import math
import re
import util.input as input
import os.path as path
from functools import reduce

DIRECTION = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, -1),
    "D": (0, 1)
}
DIRECTION_HEX = {
    0: (1, 0),
    1: (0, 1),
    2: (-1, 0),
    3: (0, -1)
}


def main():
    filepath = path.join(path.dirname(__file__), "test.txt")
    inp = input.readFromFile(filepath, True)
    part_1(inp)
    part_2(inp)


def part_1(inp: list[str]):
    row = column = 0
    instructions = list(map(lambda x: parse_instruction(x), inp))
    col_instr = map(lambda instr: instr[0][0] * instr[1], instructions)
    row_instr = map(lambda instr: instr[0][1] * instr[1], instructions)
    _, min_col, max_col = map(int, reduce(lambda x, y: (
        x[0] + y, min(x[1], y + x[0]), max(x[2], y + x[0])), col_instr, (0, math.inf, - math.inf)))
    _, min_row, max_row = map(int, reduce(lambda x, y: (
        x[0] + y, min(x[1], y + x[0]), max(x[2], y + x[0])), row_instr, (0, math.inf, - math.inf)))
    points = [[0] * ((max_col - min_col) + 1)
              for row in range(abs(max_row - min_row) + 1)]
    delta_row = (min_row)
    delta_col = (min_col)
    vertices = []
    perimeter = 0
    for direction, amount, _ in instructions:
        points[row-delta_row][column-delta_col] = 1
        vertices.append((column, row))
        perimeter += amount

        end_column = column + direction[0] * amount
        end_row = row + direction[1] * amount
        for p_y in range(min(row, end_row), max(row, end_row) + 1):
            for p_x in range(min(column, end_column), max(column, end_column) + 1):
                points[p_y-delta_row][p_x-delta_col] = 1
        row = end_row
        column = end_column

    vertices.append((column, row))

    area = shoelace(vertices) + perimeter // 2 + 1
    print(f"Part 1: {int(area)}")


def part_2(inp: list[str]):
    row = column = 0
    instructions = list(map(lambda x: parse_instruction_part_2(x), inp))
    vertices = []
    perimeter = 0
    for direction, amount, _ in instructions:
        vertices.append((column, row))
        perimeter += amount

        end_column = column + direction[0] * amount
        end_row = row + direction[1] * amount
        row = end_row
        column = end_column

    vertices.append((column, row))

    area = shoelace(vertices) + perimeter // 2 + 1
    print(f"Part 2: {int(area)}")


def shoelace(vertices):
    n = len(vertices)
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += vertices[i][0] * vertices[j][1]
        area -= vertices[j][0] * vertices[i][1]
    area = abs(area) / 2.0
    return area


def parse_instruction(instruction: str):
    [direction_string, amount_string, color_string] = instruction.split(" ")
    amount = int(amount_string)
    direction = DIRECTION[direction_string]
    color = int(color_string[2:-1], 16)
    return (direction, amount, color)


def parse_instruction_part_2(instruction: str):
    [_, _, color_string] = instruction.split(" ")
    color = color_string[2:-1]
    amount = int(color[:5], 16)
    direction = DIRECTION_HEX[int(color[-1:], 16)]
    return (direction, amount, color)


def print_points(points: list[list[int]]):
    print('\n'.join([''.join(['#' if cell == 1 else '.' for cell in row])
          for row in points]))


if __name__ == "__main__":
    main()
