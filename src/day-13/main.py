import util.input as input
import os.path as path


def main():
    filepath = path.join(path.dirname(__file__), "input.txt")
    inp = input.read_from_file_to_string(filepath, True)
    part_1(inp)
    part_2(inp)


def part_1(inp: str):
    patterns = parse_input(inp)
    sum = 0
    for pattern in patterns:
        transposed_pattern = list(zip(*pattern))
        horizontal_mirrors = find_horizontal_pattern_mirrors(pattern)
        vertical_mirrors = find_horizontal_pattern_mirrors(transposed_pattern)
        sum += 100 * horizontal_mirrors[0] if len(horizontal_mirrors) else 0
        sum += vertical_mirrors[0] if len(vertical_mirrors) else 0

    print(f"Part 1: {sum}")


def part_2(inp: str):
    patterns = parse_input(inp)
    sum = 0
    for pattern in patterns:
        transposed_pattern = list(zip(*pattern))
        horizontal_mirrors = find_horizontal_pattern_mirrors(pattern, 1)
        vertical_mirrors = find_horizontal_pattern_mirrors(
            transposed_pattern, 1)
        sum += 100 * horizontal_mirrors[0] if len(horizontal_mirrors) else 0
        sum += vertical_mirrors[0] if len(vertical_mirrors) else 0

    print(f"Part 2: {sum}")


def find_horizontal_pattern_mirrors(pattern: list[str], differences: int = 0) -> list[int]:
    above_reversed = []
    below = pattern.copy()
    mirrors: list[int] = []
    position = 0
    while len(below) > 1:
        above_reversed.insert(0, below.pop(0))
        position += 1
        # it is always true that
        # above_reversed[::-1] + below == pattern

        above_reversed_trimmed = above_reversed[:len(below):]
        below_trimmed = below[:len(above_reversed)]
        diffs: list[int] = []
        for line_a, line_b in zip(above_reversed_trimmed, below_trimmed):
            line_diff = sum(a != b for a, b in zip(line_a, line_b))
            diffs.append(line_diff)

        if sum(diffs) == differences:
            mirrors.append(position)

    return mirrors


def parse_input(inp: str) -> list[list[str]]:
    patterns = list(map(lambda x: x.split("\n"), inp.split("\n\n")))
    return patterns


if __name__ == "__main__":
    main()
