# https://adventofcode.com/2021/day/21
from __future__ import print_function
from pathlib import Path
from collections import defaultdict, Counter
from itertools import product


def game_next(pos, inc, size=10):
    return (pos - 1 + inc) % size + 1


def roll_die(die_val, count):
    total = 0
    for _ in range(3):
        die_val = game_next(die_val, 1, 100)
        total += die_val
    return total, (die_val, count + 3)


def play1(players):
    score = [0] * 2
    current, die = 0, (0, 0)
    while True:
        die_total, die = roll_die(*die)
        players[current] = game_next(players[current], die_total, 10)
        score[current] += players[current]
        if score[current] >= 1000:
            break
        current = 1 - current
    return score[1 - current] * die[1]


dirac_die_rolls = Counter(map(sum, product(range(1, 4), repeat=3)))


def try_all_games(game_state):
    new_game_state = defaultdict(int)
    score = [0] * 2
    for (p1pos, p2pos, p1score, p2score, current), n in game_state.items():
        if current == 0:
            for roll, count in dirac_die_rolls.items():
                p1_newpos = game_next(p1pos, roll)
                p1_newscore = p1score + p1_newpos
                if p1_newscore >= 21:
                    score[current] += n * count
                else:
                    new_game_state[p1_newpos, p2pos,
                                   p1_newscore, p2score, 1 - current] += n * count
        else:
            for roll, count in dirac_die_rolls.items():
                p2_newpos = game_next(p2pos, roll)
                p2_newscore = p2score + p2_newpos
                if p2_newscore >= 21:
                    score[current] += n * count
                else:
                    new_game_state[p1pos, p2_newpos,
                                   p1score, p2_newscore, 1 - current] += n * count
    return new_game_state, score


def play2(players):
    game_state = defaultdict(int)
    # initial state
    game_state[players[0], players[1], 0, 0, 0] = 1
    total_score = [0] * 2
    while game_state:
        game_state, score = try_all_games(game_state)
        total_score[0] += score[0]
        total_score[1] += score[1]
    return max(total_score)


def process(data):
    # part 1
    result = play1(data.copy())
    print("part 1:", result)
    # part 2
    result = play2(data)
    print("part 2:", result)


def parse_line(line):
    return int(line.split(': ')[1])


def load_data(fileobj):
    return [parse_line(line) for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
