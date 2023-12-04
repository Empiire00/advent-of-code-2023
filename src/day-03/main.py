from dataclasses import dataclass
import re
from os import path
import math
import util.input as input


@dataclass
class Number:
    value: int
    positions: list[tuple[int, int]]

    def includes_position(self, y: int, x: int) -> bool:
        return self.positions.count((y, x)) > 0

    def __hash__(self) -> int:
        return hash((self.value, (self.positions[0] if len(self.positions) > 0 else None)))


def main():
    filepath = path.join(path.dirname(__file__), "input.txt")
    inp = input.readFromFile(filepath, True)
    part_1(inp)
    part_2(inp)


def part_2(inp: list[str]):
    max_y = len(inp) - 1
    max_x = len(inp[0]) - 1
    numbers: list[Number] = []
    gear_positions: list[tuple[int, int]] = []
    for index, line in enumerate(inp):
        y_pos = index
        schematic_numbers = re.finditer(r"([0-9]+)", line)
        for number in schematic_numbers:
            number_pos = []
            value = int(number.group(1))
            for x_pos in range(number.start(), number.end()):
                number_pos.append((y_pos, x_pos))
            numbers.append(Number(value, number_pos))

        gears = re.finditer(r"([\*])", line)
        for part in gears:
            x_pos = part.start()
            gear_positions.append((y_pos, x_pos))

    sum_of_gear_powers = 0
    for gear_y, gear_x in gear_positions:
        included_numbers: set[Number] = set()
        # check x:  min(0, x-1); max(x+1, max_x)
        x_range = range(max(0, gear_x - 1), min(gear_x + 1, max_x) + 1)
        # check y:  min(0, y-1); max(y+1, max_y)
        y_range = range(max(0, gear_y - 1), min(gear_y + 1, max_y) + 1)
        xy_range = [(x, y) for x in x_range for y in y_range
                    if not (x == gear_x and y == gear_y)
                    ]
        for x, y in xy_range:
            for num in numbers:
                if num.includes_position(y, x):
                    included_numbers.add(num)
        if len(included_numbers) > 1:
            sum_of_gear_powers += math.prod(
                [number.value for number in included_numbers])

    print(f"Part 2: {sum_of_gear_powers}")


def part_1(inp: list[str]):
    max_y = len(inp) - 1
    max_x = len(inp[0]) - 1
    numbers: list[Number] = []
    machine_parts: list[tuple[int, int]] = []
    for index, line in enumerate(inp):
        y_pos = index
        schematic_numbers = re.finditer(r"([0-9]+)", line)
        for number in schematic_numbers:
            number_pos = []
            value = int(number.group(1))
            for x_pos in range(number.start(), number.end()):
                number_pos.append((y_pos, x_pos))
            numbers.append(Number(value, number_pos))

        engine_parts = re.finditer(r"([^.0-9])", line)
        for part in engine_parts:
            x_pos = part.start()
            machine_parts.append((y_pos, x_pos))

    numbers_belonging_to_machine_part: set[Number] = set()
    for number in numbers:
        belongs_to_machine_part = False
        for machine_part_position in machine_parts:
            # do this to break loop, if corresponding machine part has already been found
            # in inner for loop
            if belongs_to_machine_part:
                break
            y_pos, x_pos = machine_part_position
            x_range = range(max(0, x_pos - 1), min(x_pos + 1, max_x) + 1)
            y_range = range(max(0, y_pos - 1), min(y_pos + 1, max_y) + 1)
            xy_range = [(x, y) for x in x_range for y in y_range
                        if not (x == x_pos and y == y_pos)
                        ]
            for x, y in xy_range:
                # check if machine part belongs to number position
                if number.includes_position(y, x):
                    belongs_to_machine_part = True
                    break
        if belongs_to_machine_part:
            numbers_belonging_to_machine_part.add(number)

    sum_of_part_ids = sum([x.value for x in numbers_belonging_to_machine_part])

    print(f"Part 1: {sum_of_part_ids}")


if __name__ == "__main__":
    main()
