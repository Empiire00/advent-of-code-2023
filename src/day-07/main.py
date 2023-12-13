import util.input as input
import os.path as path
import re

ORDER = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2
}


def main():
    filepath = path.join(path.dirname(__file__), "input.txt")
    inp = input.readFromFile(filepath, True)
    part_1(inp)
    part_2(inp)


def part_1(inp: list[str]):
    hands_and_bets = [(card, int(bet))
                      for [card, bet] in [line.split(" ") for line in inp]]
    hands_and_bets.sort(key=lambda x: get_hand_rating(x[0]), reverse=False)
    sum = 0
    debug = [(str(hand), get_hand_rating(hand))
             for (hand, _) in hands_and_bets]
    for index, value in enumerate(hands_and_bets):
        (_, bet) = value
        add_to_sum = bet * (index + 1)
        sum += add_to_sum

    print(f"Part 1: {sum}")


def part_2(inp: list[str]):
    pass


def get_hand_rating(hand: str) -> int:
    cards = [x for x in hand]

    ind_card_rating = (15 ** 4 * ORDER[cards[0]]
                       + 15 ** 3 * ORDER[cards[1]]
                       + 15 ** 2 * ORDER[cards[2]]
                       + 15 ** 1 * ORDER[cards[3]]
                       + 15 ** 0 * ORDER[cards[4]]
                       )
    streak_rating = 15 ** 10 * streak(hand)
    score = ind_card_rating + streak_rating
    return score


def streak(hand: str) -> int:
    cards = [x for x in hand]
    cards.sort()

    cards_count = {card: cards.count(card) for card in set(cards)}
    counts = list(cards_count.values())
    counts.sort(reverse=True)

    # five of a kind
    if counts == [5]:
        # print(hand + ": 5 of a kind")
        return 7
    # four of a kind
    elif counts == [4, 1]:
        # print(hand + ": 4 of a kind")
        return 6
    # full house
    elif counts == [3, 2]:
        # print(hand + ": Full house")
        return 5
    # 3 of a kind
    elif counts == [3, 1, 1]:
        # print(hand + ": 3 of a kind")
        return 4
    # two pair
    elif counts == [2, 2, 1]:
        # print(hand + ": 2 pairs")
        return 3
    # one pair
    elif counts == [2, 1, 1, 1]:
        # print(hand + ": 1 pair")
        return 2
    # high card
    else:
        # print(hand + ": high card")
        return 1


def get_high_card(hand: str) -> int:
    return max(ORDER[card] for card in hand)


if __name__ == "__main__":
    main()
