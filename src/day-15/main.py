import re
import util.input as input
import os.path as path
from functools import reduce


def main():
    filepath = path.join(path.dirname(__file__), "input.txt")
    inp = input.read_from_file_to_string(filepath, True)
    part_1(inp)
    part_2(inp)


def part_1(inp: str):
    input_list: list[str] = inp.split(",")
    sum = 0
    for string in input_list:
        sum += hash_string(string)
    print(f"Part 1: {sum}")


def part_2(inp: str):
    input_list: list[str] = inp.split(",")
    # boxes: []Box
    #   Box: []Lens
    #       Lens: Tuple[Label, FocalLength]
    #           Label: str
    #           FocalLength: int
    boxes: list[list[tuple[str, int]]] = [[] for x in range(0, 256)]
    for instruction in input_list:
        label_match = re.search(r"(.+)[-=]", instruction)
        assert (label_match is not None)
        label = label_match.group(1)
        box_id: int = hash_string(label)
        box = boxes[box_id]
        if "-" in instruction:
            for index, lens in enumerate(box):
                lab, _ = lens
                if lab == label:
                    box.pop(index)
                    break
        elif "=" in instruction:
            focal_length_match = re.search(r"[-=](\d+)", instruction)
            assert (focal_length_match is not None)
            focal_length = int(focal_length_match.group(1))

            # add/replace lens in box
            inserted = False
            for index, lens in enumerate(box):
                lab, _ = lens
                if lab == label:
                    box.pop(index)
                    box.insert(index, (label, focal_length))
                    inserted = True
                    break
            if not inserted:
                box.append((label, focal_length))
    sum_of_focussing_power = get_boxes_sum(boxes)
    print(f"Part 2: {sum_of_focussing_power}")


def hash_string(inp: str) -> int:
    return reduce(lambda a, b: ((int(a) + ord(b)) * 17) % 256, inp, 0)


def get_boxes_sum(boxes: list[list[tuple[str, int]]]) -> int:
    sum = 0
    for box_index, box in enumerate(boxes):
        for lens_index, lens in enumerate(box):
            _, focal_length = lens
            sum += (box_index + 1) * (lens_index + 1) * focal_length
    return sum


if __name__ == "__main__":
    main()
