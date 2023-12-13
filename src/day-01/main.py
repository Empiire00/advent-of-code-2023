import util.input as input
import re
from os import path
from functools import reduce

NUMBERS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}


def main():
    filepath = path.join(path.dirname(__file__), "input.txt")
    inp = input.readFromFile(filepath, True)
    part_1(inp)
    part_2(inp)


def part_1(inp: list[str]):
    digits = list(map(lambda line: get_digits(line), inp))
    numbers = list(map(lambda d: get_number(d[0], d[-1]), digits))
    solution = sum(numbers)
    print(f'Part 1: {solution}')


def part_2(inp: list[str]):
    digits = list(map(lambda line: get_digits_part_2(line), inp))
    numbers = list(map(lambda d: get_number(d[0], d[-1]), digits))
    solution = sum(numbers)
    print(f'Part 2: {solution}')


def get_number(*digits: int | str) -> int:
    reduced = reduce(lambda a, b: int(f"{a}{b}"), digits)
    return int(reduced)


def is_digit(to_test: str) -> bool:
    return re.match(r"(\d)", to_test) is not None


def get_digits(line: str) -> list[int]:
    digits = [int(char) for char in line if is_digit(char)]
    return digits


def get_digits_part_2(line: str) -> list[int]:
    # I know this is a bit overkill
    # In theory, there could be overlaps, e.g. twone -> which is 21
    # if the string consists of "zwctwonez", replacing will result in one digit disappearing
    # The overlap is 1 at max, so replacing "one" with "o1e" might be a valid approach, too
    digits_position: dict[int, int] = {}
    # populate "normal" digits, e.g. "1", "2"
    for index, value in enumerate(line):
        if is_digit(value):
            digits_position[index] = int(value)

    for key, value in NUMBERS.items():
        matches = re.finditer(f"({key})", line, re.IGNORECASE)
        for match in matches:
            digits_position[match.start()] = value
    # return the sorted digits (by order)
    return [digit for _, digit in sorted(digits_position.items())]


if __name__ == "__main__":
    main()
