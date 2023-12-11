import util.input as input
import os.path as path
import re
from math import lcm


def main():
    filepath = path.join(path.dirname(__file__), "input.txt")
    inp = input.readFromFile(filepath, True)
    part_1(inp)
    part_2(inp)


def part_1(inp: list[str]):
    move_instructions = inp[0]
    START = "AAA"
    END = "ZZZ"
    move_strings = inp[2::]
    move_set: tuple[str, str] = {}
    for move_str in move_strings:
        [source, choices] = list(map(str.strip, move_str.split("=")))
        choices = re.sub(r"[()]", "", choices)
        [left, right] = list(map(str.strip, choices.split(",")))
        move_set[source] = (left, right)

    arrived = False
    curr_pos = START
    steps = 0
    while not arrived:
        next_move = move_instructions[steps % len(move_instructions)]
        if next_move == "L":
            curr_pos = move_set.get(curr_pos)[0]
        elif next_move == "R":
            curr_pos = move_set.get(curr_pos)[1]
        steps += 1
        arrived = curr_pos == END

    print(f"Part 1: {steps}")


def part_2(inp: str):
    move_instructions = inp[0]
    move_strings = inp[2::]
    move_set: dict[str, str] = {}
    starts: list[str] = []
    ends: list[str] = []
    for move_str in move_strings:
        [source, choices] = list(map(str.strip, move_str.split("=")))
        choices = re.sub(r"[()]", "", choices)
        [left, right] = list(map(str.strip, choices.split(",")))
        move_set[source] = (left, right)
        if source.endswith("A"):
            starts.append(source)
        elif source.endswith("Z"):
            ends.append(source)

    curr_positions = starts.copy()
    steps_arr = []
    for position in curr_positions:
        steps = 0
        curr_pos = position
        arrived = False
        while not arrived:
            next_move = move_instructions[steps % len(move_instructions)]
            if next_move == "L":
                curr_pos = move_set.get(curr_pos)[0]
            elif next_move == "R":
                curr_pos = move_set.get(curr_pos)[1]
            arrived = ends.count(curr_pos) == 1
            steps += 1
        steps_arr.append(steps)

    # take least common multiple of steps
    lcm_steps = lcm(*steps_arr)
    print(f"Part 2: {lcm_steps}")


if __name__ == "__main__":
    main()
