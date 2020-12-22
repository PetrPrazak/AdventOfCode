# https://adventofcode.com/2020/day/22
from __future__ import print_function
from collections import deque
from copy import copy, deepcopy
from itertools import islice

def add_cards(deck, winning, losing):
    deck.append(winning)
    deck.append(losing)


def play(deck1, deck2):
    while deck1 and deck2:
        card1, card2 = deck1.popleft(), deck2.popleft()
        if card1 > card2:
            add_cards(deck1, card1, card2)
        else:
            add_cards(deck2, card2, card1)
    return deck1 if deck1 else deck2


def copy_deck(deck, length):
    return deque(islice(deck, 0, length))


def compare_decks(deck1, deck2):
    return set(deck1) == set(deck2)


def repeated(prev_games, deck1, deck2):
    for prev_deck1, prev_deck2 in prev_games:
        if compare_decks(deck1, prev_deck1) and compare_decks(deck2, prev_deck2):
            return True
    return False


def rec_play(deck1, deck2, level=0):
    prev_games = []
    while deck1 and deck2:
        if repeated(prev_games, deck1, deck2):
            break
        prev_games.append((copy(deck1), copy(deck2)))

        card1, card2 = deck1.popleft(), deck2.popleft()
        if card1 <= len(deck1) and card2 <= len(deck2):
            if rec_play(copy_deck(deck1, card1), copy_deck(deck2, card2), level+1):
                add_cards(deck1, card1, card2)
            else:
                add_cards(deck2, card2, card1)
        else:
            if card1 > card2:
                add_cards(deck1, card1, card2)
            else:
                add_cards(deck2, card2, card1)

    if level:
        return bool(deck1)
    else:
        return deck1 if deck1 else deck2


def sum_deck(deck):
    return sum((i+1) * c for i, c in enumerate(reversed(deck)))


def process(data):
    part1data = deepcopy(data)
    winner = play(*part1data)
    # part 1
    result = sum_deck(winner)
    print("part 1:", result)
    # part 2
    winner = rec_play(*data)
    result = sum_deck(winner)
    print("part 2:", result)


def parse_player(line):
    _, *data = line.split("\n")
    return deque(int(n) for n in data)


def load_data(fileobj):
    return [parse_player(player.rstrip()) for player in fileobj.read().split("\n\n")]


def main(file):
    print(file)
    with open(file) as f:
        process(load_data(f))


if __name__ == "__main__":
    main("test.txt")
    main("input.txt")
