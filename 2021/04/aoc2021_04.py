# https://adventofcode.com/2021/day/4
from __future__ import print_function
from pathlib import Path


def check_bingo_row(card, card_found):
    for row in range(5):
        row_idx = row * 5
        card_row = card[row_idx:row_idx+5]
        if all(num in card_found for num in card_row):
            return True
    return False


def check_bingo_col(card, card_found):
    for col in range(5):
        column = (card[row * 5 + col] for row in range(5))
        if all(num in card_found for num in column):
            return True
    return False


def check_bingo(card, card_found):
    return check_bingo_row(card, card_found) or check_bingo_col(card, card_found)


def find_bingo(draw, cards, cards_found):
    for card_idx, card in enumerate(cards):
        if draw in card:
            cards_found[card_idx].add(draw)
    for card_idx, card in enumerate(cards):
            if check_bingo(card, cards_found[card_idx]):
                return card_idx
    return None


def part1(data):
    draws, cards = data
    cards_found = [set() for _ in range(len(cards))]
    for draw in draws:
        if (bingo_idx := find_bingo(draw, cards, cards_found)) is not None:
            return draw, cards[bingo_idx], cards_found[bingo_idx]
    return None, None, None


def part2(data):
    draws, cards = data
    cards_found = [set() for _ in range(len(cards))]
    for draw in draws:
        while (bingo_idx := find_bingo(draw, cards, cards_found)) is not None:
            if len(cards) == 1:
                return draw, cards[0], cards_found[0]
            del cards[bingo_idx]
            del cards_found[bingo_idx]
    return None, None, None


def process(data):
    # part 1
    last_draw, card, found = part1(data)
    non_drawn_numbers = sum(card) - sum(found)
    result = last_draw * non_drawn_numbers
    print("part 1:", result)
    # part 2
    last_draw, card, found = part2(data)
    non_drawn_numbers = sum(card) - sum(found)
    result = last_draw * non_drawn_numbers
    print("part 2:", result)


def load_data(fileobj):
    draws, *cards = fileobj.read().split("\n\n")
    draws = [int(number) for number in draws.split(',')]
    cards = [[int(number) for number in card.split()] for card in cards]
    return draws, cards


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
