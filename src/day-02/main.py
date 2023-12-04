from dataclasses import dataclass
import re
from os import path
import util.input as input


@dataclass
class Game:
    red: int
    green: int
    blue: int

    def is_possible(self, game) -> bool:
        return (
            self.red <= game.red and self.green <= game.green and self.blue <= game.blue
        )


def main():
    filepath = path.join(path.dirname(__file__), "input.txt")
    inp = input.readFromFile(filepath, True)
    part_1(inp)
    part_2(inp)


def part_1(inp: list[str]):
    master_game = Game(12, 13, 14)
    possible_game_sets = get_game_sets(inp, master_game)
    sum_of_possible_ids = 0
    for id in possible_game_sets.keys():
        sum_of_possible_ids += id

    print(f"Part 1: {sum_of_possible_ids}")


def part_2(inp: list[str]):
    master_game = Game(12, 13, 14)
    game_sets = get_game_sets(inp, master_game, return_impossible=True)

    sum_of_power = 0
    # get least possible amount of game colors
    for set in game_sets.values():
        min_red = max([game.red for game in set])
        min_blue = max([game.blue for game in set])
        min_green = max([game.green for game in set])
        power_of_set = min_red * min_blue * min_green
        sum_of_power += power_of_set

    print(f"Part 2: {sum_of_power}")


def get_game_sets(
    inp: list[str], master_game: Game, return_impossible=False
) -> dict[int, list[Game]]:
    game_sets: dict[int, list[Game]] = dict()
    for line in inp:
        id, game_strings = parse_line(line)
        games = [parse_game_string(game_string)
                 for game_string in game_strings]
        sub_games: list[Game] = [
            game for game in games if game.is_possible(master_game)
        ]
        all_possible = len(games) == len(sub_games)
        if return_impossible or all_possible:
            game_sets[id] = games

    return game_sets


def parse_game_string(game_string: str) -> Game:
    blue, red, green = "0", "0", "0"
    blue_match = re.search(r"(\d+)[\s]*blue", game_string)
    red_match = re.search(r"(\d+)[\s]*red", game_string)
    green_match = re.search(r"(\d+)[\s]*green", game_string)
    if blue_match is not None:
        blue = blue_match.group(1)
    if green_match is not None:
        green = green_match.group(1)
    if red_match is not None:
        red = red_match.group(1)

    return Game(red=int(red), green=int(green), blue=int(blue))


# returns id and games for that id
def parse_line(line: str) -> tuple[int, list[str]]:
    matches: re.Match[str] = re.match(r"Game\s(\d+): (.+)", line)
    id = int(matches.group(1))
    games = matches.group(2)
    games = list(map(lambda x: x.strip(), games.strip().split(";")))
    return id, games


if __name__ == "__main__":
    main()
