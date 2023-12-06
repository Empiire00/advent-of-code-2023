import util.input as input
import os.path as path
import re


def main():
    filepath = path.join(path.dirname(__file__), "input.txt")
    inp = input.read_from_file_to_string(filepath)
    part_1(inp)
    part_2(inp)


def part_1(inp: str):
    times_str = re.search(r"Time:[\s\t]+(.+)\n", inp).group(1)
    distances_str = re.search(r"Distance:[\s\t]+(.+)", inp).group(1)
    times = re.sub(r"\s+", " ", times_str).split(" ")
    distances = re.sub(r"\s+", " ", distances_str).split(" ")

    prod = 1
    for time, distance in zip(map(int, times), map(int, distances)):
        ways = 0
        for i in range(1, time):
            if calculate_distance(i, time) > distance:
                ways += 1
        prod *= 1 if ways == 0 else ways

    print(f"Part 1: {prod}")


def part_2(inp: str):
    times_str = re.search(r"Time:[\s\t]+(.+)\n", inp).group(1)
    distances_str = re.search(r"Distance:[\s\t]+(.+)", inp).group(1)
    times = re.sub(r"\s+", "", times_str).split(" ")
    distances = re.sub(r"\s+", "", distances_str).split(" ")

    prod = 1
    for time, distance in zip(map(int, times), map(int, distances)):
        ways = 0
        for i in range(1, time):
            if calculate_distance(i, time) > distance:
                ways += 1
        prod *= 1 if ways == 0 else ways

    print(f"Part 2: {prod}")


def calculate_distance(holding_time: int, time: int) -> int:
    speed = holding_time
    acceleration_time = time - holding_time
    return acceleration_time * speed


if __name__ == "__main__":
    main()
