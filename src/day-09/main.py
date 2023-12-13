from typing import Any
import util.input as input
import os.path as path


def main():
    filepath = path.join(path.dirname(__file__), "input.txt")
    inp = input.readFromFile(filepath, True)
    part_1(inp)
    part_2(inp)


def part_1(inp: list[str]):
    predictions: list[int] = []
    for line in inp:
        differences = calculate_differences(line)
        predictions.append(predict_after(differences))

    print(f"Part 1: {sum(predictions)}")


def part_2(inp: list[str]):
    predictions: list[int] = []
    for line in inp:
        differences = calculate_differences(line)
        predictions.append(predict_before(differences))

    print(f"Part 2: {sum(predictions)}")


def calculate_differences(line: str):
    values: list[int] = list(map(int, line.split(" ")))
    differences: list[list[Any]] = [values.copy()]
    index: int = 1
    while True:
        differences.append([None]*(len(differences[index - 1]) - 1))
        for i in range(1, len(differences[index - 1])):
            right = differences[index - 1][i]
            left = differences[index - 1][i - 1]
            differences[index][i - 1] = right - left
        if (all(diff == 0 for diff in differences[index])):
            break
        index += 1
    return differences


def predict_after(data: list[list[int]]) -> int:
    copy = data.copy()
    copy.reverse()
    last: int = copy[1][-1]
    for i in range(2, len(copy)):
        last = copy[i][-1] + last
    return last


def predict_before(data: list[list[int]]) -> int:
    copy = data.copy()
    copy.reverse()
    last: int = copy[1][0]
    for i in range(2, len(copy)):
        last = copy[i][0] - last
    return last


if __name__ == "__main__":
    main()
