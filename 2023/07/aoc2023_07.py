# https://adventofcode.com/2023/day/7
from pathlib import Path
from collections import Counter
import time

CARDS = {c: v for v, c in enumerate("23456789TJQKA", 1)}
CARDS_BASE = len(CARDS)
CARDS_JOKER = {c: v for v, c in enumerate("J23456789TQKA", 1)}


def value(hand, joker=False):
    val = 0
    mapping = CARDS_JOKER if joker else CARDS
    for c in hand:
        val = val * CARDS_BASE + mapping[c]
    return val


def strength(hand):
    cc = Counter(hand)
    match len(cc):
        case 1:
            # five of kind
            return 7
        case 2:
            # 4 + 1 - four of a kind or a full house
            return 6 if 4 in cc.values() else 5
        case 3:
            # either three of kind or two pair
            return 4 if 3 in cc.values() else 3
        case 4:
            # one pair
            return 2
        case 5:
            # all distinct
            return 1
    return 0


def strength_joker(hand):
    cards = set(hand)
    if not 'J' in cards:
        return strength(hand)
    cards.remove('J')
    if not cards:
        # all J's
        return 7
    return max(strength(hand.replace('J', l)) for l in cards)


def hand_value(card_data):
    hand, _ = card_data
    return strength(hand), value(hand)


def hand_value_joker(card_data):
    hand, _ = card_data
    return strength_joker(hand), value(hand, joker=True)


def solve(data, key=hand_value):
    return sum(bid * idx for idx, (_, bid) in enumerate(sorted(data, key=key), 1))


def process(data):
    # part 1
    result = solve(data)
    print("part 1:", result)
    # part 2
    result = solve(data, key=hand_value_joker)
    print("part 2:", result)


def parse_line(line):
    hand, bid = line.split()
    return hand, int(bid)


def load_data(fileobj):
    return [parse_line(line.rstrip()) for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        t1 = time.perf_counter()
        process(load_data(f))
        t2 = time.perf_counter()
        print(f"Finished in {t2 - t1:.3f} s")


if __name__ == "__main__":
    # main("test.txt")
    main()
