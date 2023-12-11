import re
import util.input as input
import os.path as path


def main():
    filepath = path.join(path.dirname(__file__), "input.txt")
    inp = input.readFromFile(filepath, True)
    part_1(inp)
    part_2(inp)


def part_1(inp: list[str]):
    galaxy_positions, empty_cols, empty_rows = parse_input(inp)

    # sort by y-coordinate to ease up permutations
    # in fact, this should be done already, since we parsed line by line
    # do it anyways
    galaxy_positions.sort(key=lambda galaxy_pos: galaxy_pos[1])

    sum_distances_before_expansion = calculate_distances(galaxy_positions)

    # add spaces <-> expand empty lines/columns
    # get amount of separated galaxy routes e.g. A ->...-> x_space -> ... -> y_space -> ... B
    additional_distance_x = calculate_additional_distance_for_axis(
        galaxy_positions, empty_cols, 0)
    additional_distance_y = calculate_additional_distance_for_axis(
        galaxy_positions, empty_rows, 1)

    overall_sum = sum_distances_before_expansion + \
        additional_distance_x + additional_distance_y
    print(f"Part 1: {overall_sum}")


def part_2(inp: str):
    galaxy_positions, empty_cols, empty_rows = parse_input(inp)

    # sort by y-coordinate to ease up permutations
    # in fact, this should be done already, since we parsed line by line
    # do it anyways
    galaxy_positions.sort(key=lambda galaxy_pos: galaxy_pos[1])

    sum_distances_before_expansion = calculate_distances(galaxy_positions)

    # add spaces <-> expand empty lines/columns
    # get amount of separated galaxy routes e.g. A ->...-> x_space -> ... -> y_space -> ... B
    additional_distance_x = (1000000-1) * \
        calculate_additional_distance_for_axis(galaxy_positions, empty_cols, 0)
    additional_distance_y = (1000000-1) * \
        calculate_additional_distance_for_axis(galaxy_positions, empty_rows, 1)

    overall_sum = sum_distances_before_expansion + \
        additional_distance_x + additional_distance_y
    print(f"Part 2: {overall_sum}")


def parse_input(inp: list[str]):
    non_empty_rows: set[int] = set()
    non_empty_cols: set[int] = set()
    galaxy_positions: list[tuple[int, int]] = []
    for index, line in enumerate(inp):
        y = index
        row_empty: bool = True
        galaxies = re.finditer(r"(#)", line)
        for galaxy in galaxies:
            x = galaxy.start()
            row_empty = False
            non_empty_cols.add(x)
            galaxy_positions.append((x, y))
        if not row_empty:
            non_empty_rows.add(y)

    empty_cols: list[int] = [x for x in range(
        0, len(inp[0])) if x not in non_empty_cols]
    empty_rows: list[int] = [y for y in range(
        0, len(inp)) if y not in non_empty_rows]

    return galaxy_positions, empty_cols, empty_rows


def calculate_distances(galaxy_positions):
    sum_distances_before_expansion = 0
    for index, galaxy_pos in enumerate(galaxy_positions):
        # source_x, source_y = galaxy_pos
        dest_galaxies = galaxy_positions[index + 1::]
        distances = [calculate_distance(galaxy_pos, gal)
                     for gal in dest_galaxies]
        sum_distances_before_expansion += sum(distances)
    return sum_distances_before_expansion


def calculate_additional_distance_for_axis(galaxy_positions: list[tuple[int, int]], expanding_points: list[int], axis: int) -> int:
    """Calculates additional space for axis using separation of points. 

    Args:
        galaxy_positions (list[tuple[int,int]]): List of galaxy positions
        expanding_points (list[int]): List of coordinates, which should be expanded. Those are empty lines/columns
        axis (int): Dimension of axis. E.g. 0 for x-Axis

    Returns:
        int: Amount of extra space, that results, when space is extended by 1
    """
    additional_distance = 0
    galaxy_axis = [pos[axis] for pos in galaxy_positions]
    galaxies_on_value = {gal_axis: galaxy_axis.count(
        gal_axis) for gal_axis in set(galaxy_axis)}
    for cut in expanding_points:
        above_cut = [amount for (pos, amount)
                     in galaxies_on_value.items() if pos < cut]
        below_cut = [amount for (pos, amount)
                     in galaxies_on_value.items() if pos > cut]
        additional_distance += sum(above_cut) * sum(below_cut)
    return additional_distance


def calculate_distance(source: tuple[int, int], destination: tuple[int, int]):
    src_x, src_y = source
    dest_x, dest_y = destination
    delta_x = abs(dest_x - src_x)
    delta_y = abs(dest_y - src_y)
    return delta_x + delta_y


if __name__ == "__main__":
    main()
