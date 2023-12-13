from dataclasses import dataclass
import util.input as input
import os.path as path
import re


@dataclass
class ScratchCard:
    chosen_numbers: list[int]
    winning_numbers: list[int]
    win_ticket_ids: list[int]


def main():
    filepath = path.join(path.dirname(__file__), "input.txt")
    inp = input.readFromFile(filepath, True)
    part_1(inp)
    part_2(inp)


def part_1(inp: list[str]):
    card_values = []
    for line in inp:
        _, card_numbers, winning_numbers = parse_line(line)
        matches, _ = check_game(card_numbers, winning_numbers)
        card_values.append(2**(matches-1) if matches > 0 else 0)

    sum_of_card_values = sum(card_values)
    print(f"Part 1: {sum_of_card_values}")


def part_2(inp: list[str]):
    # maps id -> amount
    round_wins = []
    scratchcard_deck: dict[int, tuple[ScratchCard, int]] = dict()
    # first round
    for line in inp:
        id, card_numbers, winning_numbers = parse_line(line)
        matches, _ = check_game(card_numbers, winning_numbers)
        card_wins = list(range(min(id + 1, len(inp) + 1),
                               min(id + matches + 1, len(inp) + 1)))
        scratchcard: ScratchCard = ScratchCard(
            card_numbers, winning_numbers, card_wins)
        round_wins.extend(card_wins)
        scratchcard_deck[id] = (scratchcard, 1)

    # process rounds until no more winnings
    while len(round_wins) > 0:
        card_id = round_wins.pop()
        card, previous_amount = scratchcard_deck[card_id]
        scratchcard_deck[card_id] = (card, previous_amount + 1)
        round_wins.extend(card.win_ticket_ids)

    card_amounts = [amount for _, amount in list(scratchcard_deck.values())]
    print(f"Part 2: {sum(card_amounts)}")


def check_game(game_numbers: list[int], winning_numbers: list[int]) -> tuple[int, list[int]]:
    matching_numbers = [
        number for number in game_numbers if number in winning_numbers]
    return len(matching_numbers), matching_numbers


def parse_line(line: str) -> tuple[int, list[int], list[int]]:
    line = re.sub(r"[\t\s]+", " ", line)
    matches = re.match(r"Card[\s]+(\d+): (.+) \| (.+)", line)
    assert (matches is not None)
    id = int(matches.group(1))
    card_numbers = list(map(lambda s: int(s), matches.group(2).split(" ")))
    winning_numbers = list(map(lambda s: int(s), matches.group(3).split(" ")))
    return id, card_numbers, winning_numbers


if __name__ == "__main__":
    main()
