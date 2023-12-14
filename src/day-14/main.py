import util.input as input
import os.path as path


def main():
    filepath = path.join(path.dirname(__file__), "input.txt")
    inp = input.readFromFile(filepath, True)
    part_1(inp)
    part_2(inp)


def part_1(inp: list[str]):
    rocks = inp
    rocks = tilt_north(rocks)
    load = count_rocks(rocks)
    print(f"Part 1: {load}")


def part_2(inp: list[str]):
    rocks = inp
    # state_string -> count_of_occurence
    seen_states: dict[str, int] = {}
    cycle_count = 0
    total_cycles = 1000000000

    while cycle_count < total_cycles:
        rocks = tilt_north(rocks)
        rocks = tilt_west(rocks)
        rocks = tilt_south(rocks)
        rocks = tilt_east(rocks)
        cycle_count += 1

        state_str = state_to_string(rocks)
        if state_str in seen_states:
            # get the length of the cycle based on the past iteration this state was detected
            cycle_length = cycle_count - seen_states[state_str]
            remaining_cycles = (total_cycles - cycle_count) % cycle_length

            # Run the remaining cycles
            for _ in range(remaining_cycles):
                rocks = tilt_north(rocks)
                rocks = tilt_west(rocks)
                rocks = tilt_south(rocks)
                rocks = tilt_east(rocks)
            break
        else:
            seen_states[state_str] = cycle_count

    load = count_rocks(rocks)
    print(f"Part 2: {load}")


def tilt(rocks, direction):
    height, width = len(rocks), len(rocks[0])

    if direction in ['north', 'south']:
        for col in range(width):
            column = [rocks[row][col] for row in range(height)]
            if direction == 'south':
                column.reverse()

            new_column = move_rocks(column)

            if direction == 'south':
                new_column.reverse()
            for row in range(height):
                rocks[row] = rocks[row][:col] + \
                    new_column[row] + rocks[row][col + 1:]
    else:
        for row in range(height):
            line = list(rocks[row])
            if direction == 'east':
                line.reverse()

            new_line = move_rocks(line)

            if direction == 'east':
                new_line.reverse()

            rocks[row] = ''.join(new_line)

    return rocks


def move_rocks(line):
    new_line = list(line)
    for i in range(len(line)):
        if line[i] == 'O':
            j = i
            while j > 0 and new_line[j - 1] == '.':
                j -= 1
            if j != i:
                new_line[i] = '.'
                new_line[j] = 'O'
    return new_line


def tilt_north(rocks):
    return tilt(rocks, 'north')


def tilt_south(rocks):
    return tilt(rocks, 'south')


def tilt_east(rocks):
    return tilt(rocks, 'east')


def tilt_west(rocks):
    return tilt(rocks, 'west')


def state_to_string(rocks):
    return '\n'.join(rocks)


def count_rocks(rocks: list[str]):
    overall_sum = 0
    for row_index, row in enumerate(rocks[::-1]):
        overall_sum += (row_index + 1) * sum(1 for x in row if x == "O")
    return overall_sum


if __name__ == "__main__":
    main()
