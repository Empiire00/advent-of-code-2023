from collections import deque
import util.input as input
import os.path as path


def main():
    filepath = path.join(path.dirname(__file__), "input.txt")
    inp = input.readFromFile(filepath, True)
    part_1(inp)
    part_2(inp)


def part_1(inp: list[str]):
    mirror_grid = parse_input(inp)
    answer = get_amount_of_energized_beams(mirror_grid, (0, 0, "R"))
    print(f"Part 1: {answer}")


def part_2(inp: list[str]):
    mirror_grid = parse_input(inp)
    rows = len(mirror_grid)
    cols = len(mirror_grid[0])
    starting_points = [(0, x, "D") for x in range(cols)] + \
        [(y, 0, "R") for y in range(rows)] + \
        [(rows - 1, x, "U") for x in range(cols)] + \
        [(y, cols - 1, "L") for y in range(rows)]
    answer = max(get_amount_of_energized_beams(mirror_grid, starting_pos)
                 for starting_pos in starting_points)
    print(f"Part 2: {answer}")


def get_amount_of_energized_beams(mirror_grid, starting_position):
    beams_grid = [[[] for l in range(len(mirror_grid[0]))]
                  for x in range(len(mirror_grid))]
    # test_grid = [[mirror_grid[x][l] for l in range(len(mirror_grid[0]))]
    #             for x in range(len(mirror_grid))]

    queue = deque()
    queue.append(starting_position)
    while queue:
        todo = queue.pop()
        y, x, direction = todo
        next_pos = None
        if direction in beams_grid[y][x]:
            continue
        beams_grid[y][x].append(direction)
        # test_grid[y][x] = "#"
        next_directions = get_next_direction(mirror_grid, direction, (y, x))
        for new_direction in next_directions:
            if new_direction == "R":
                if x + 1 < len(beams_grid[0]):
                    next_pos = (y, x + 1)
            elif new_direction == "L":
                if x - 1 >= 0:
                    next_pos = (y, x - 1)
            elif new_direction == "D":
                if y + 1 < len(beams_grid):
                    next_pos = (y + 1, x)
            elif new_direction == "U":
                if y - 1 >= 0:
                    next_pos = (y - 1, x)

            if next_pos is not None:
                queue.append((next_pos[0], next_pos[1], new_direction))

    energized_beams = 0
    for row in beams_grid:
        energized_beams += sum(1 for cell in row if len(cell))
    # print("".join(["".join(line) for line in test_grid]))
    return energized_beams


def get_next_direction(grid, direction: str, position: tuple[int, int]) -> list[str]:
    y, x = position
    if grid[y][x] == "|":
        if direction in ["R", "L"]:
            return ["U", "D"]
        else:
            return [direction]
    elif grid[y][x] == "-":
        if direction in ["U", "D"]:
            return ["R", "L"]
        else:
            return [direction]
    elif grid[y][x] == "\\":
        if direction in ["U", "R"]:
            return ["L"] if direction == "U" else ["D"]
        elif direction in ["D", "L"]:
            return ["U"] if direction == "L" else ["R"]
    elif grid[y][x] == "/":
        if direction in ["D", "R"]:
            return ["U"] if direction == "R" else ["L"]
        elif direction in ["U", "L"]:
            return ["D"] if direction == "L" else ["R"]
    elif grid[y][x] == ".":
        return [direction]

    return []


def parse_input(inp: list[str]):
    return [list(line) for line in inp]


if __name__ == "__main__":
    main()
