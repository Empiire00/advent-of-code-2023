from dataclasses import dataclass
import math
from multiprocessing import Pool
import util.input as input
import os.path as path
import re
from functools import partial
from tqdm.auto import tqdm


@dataclass
class ConversionMapping:
    src_start: int
    dest_start: int
    length: int


class ConversionDict:
    mappings: list[ConversionMapping]
    cache: dict[int, int] = {}

    def __init__(self, mappings: list[ConversionMapping], use_cache: bool = False) -> None:
        self.mappings = mappings
        self.mappings.sort(key=lambda mapping: mapping.src_start)
        self.use_cache = use_cache

    def get(self, src_value: int) -> int:
        val: int = src_value
        for mapping in self.mappings:
            # sorted list of mappings, so we can break
            if mapping.src_start > src_value:
                break
            if mapping.src_start <= src_value <= mapping.src_start + mapping.length:
                delta = src_value - mapping.src_start
                val = mapping.dest_start + delta
        return val


def main():
    filepath = path.join(path.dirname(__file__), "input.txt")
    inp = input.read_from_file_to_string(filepath)
    part_1(inp)
    part_2(inp)


def get_conversion_dict(conversion_str: str) -> ConversionDict:
    mappings: list[ConversionMapping] = []
    for conv_rule in conversion_str.split("\n"):
        parts = conv_rule.split(" ")
        # parts: [dest_start, src_start, range_length]
        dest, src, length = int(parts[0]), int(parts[1]), int(parts[2])
        mappings.append(ConversionMapping(src, dest, length))
    return ConversionDict(mappings)


def get_conversion_dicts(inp: str) -> list[ConversionDict]:
    seed_to_soil_str = re.search(
        r"seed-to-soil map:\n([\s\d]+)\n\n", inp).group(1)
    soil_to_fert_str = re.search(
        r"soil-to-fertilizer map:\n([\s\d]+)\n\n", inp).group(1)
    fert_to_water_str = re.search(
        r"fertilizer-to-water map:\n([\s\d]+)\n\n", inp).group(1)
    water_to_light_str = re.search(
        r"water-to-light map:\n([\s\d]+)\n\n", inp).group(1)
    light_to_temp_str = re.search(
        r"light-to-temperature map:\n([\s\d]+)\n\n", inp).group(1)
    temp_to_humid_str = re.search(
        r"temperature-to-humidity map:\n([\s\d]+)\n\n", inp).group(1)
    humid_to_loc_str = re.search(
        r"humidity-to-location map:\n([\s\d]+)", inp).group(1)

    seed_to_soil = get_conversion_dict(seed_to_soil_str)
    soil_to_fert = get_conversion_dict(soil_to_fert_str)
    fert_to_water = get_conversion_dict(fert_to_water_str)
    water_to_light = get_conversion_dict(water_to_light_str)
    light_to_temp = get_conversion_dict(light_to_temp_str)
    temp_to_humid = get_conversion_dict(temp_to_humid_str)
    humid_to_loc = get_conversion_dict(humid_to_loc_str)

    conversions = [
        seed_to_soil, soil_to_fert,
        fert_to_water, water_to_light,
        light_to_temp, temp_to_humid,
        humid_to_loc
    ]
    return conversions


def chain_conversions(input: int, dicts: ConversionDict) -> int:
    curr: int = input
    for d in dicts:
        curr = d.get(curr)
    return curr


def part_1(inp: str):
    seeds_str = re.search(r"seeds:\s([\d\s]+)", inp).group(1).strip()
    seeds = [int(x) for x in seeds_str.split()]
    seed_locations = []
    conversions = get_conversion_dicts(inp)
    seed_locations = list(
        map(lambda seed: chain_conversions(seed, conversions), seeds))

    print(f"Part 1: {min(seed_locations)}")


def part_2(inp: str):
    seeds_str = re.search(r"seeds:\s([\d\s]+)", inp).group(1).strip()
    seed_ranges = [range(int(start), int(start)+int(length))
                   for (start, length) in zip(seeds_str.split()[0::2], seeds_str.split()[1::2])]

    conversions = get_conversion_dicts(inp)
    min_loc: int = math.inf
    print("Starting to brute-force part 2. This is going to take a while...")
    print("You might want to get a coffee or some tea\n")
    with tqdm(desc="Main loop (seed ranges)", total=len(seed_ranges)) as pbar_main:
        for s in seed_ranges:
            pool = Pool()
            with pool as p:
                with tqdm(desc=f"Seed range loop", total=len(s), leave=False) as pbar:
                    for res in p.imap_unordered(partial(process_iterable, conversions=conversions), s, chunksize=2500000):
                        min_loc = min(min_loc, res)
                        pbar.update()
            pbar_main.update()
    print(f"Part 2: {min_loc}")


def process_iterable(iter, conversions):
    return chain_conversions(iter, conversions)


if __name__ == "__main__":
    main()
