# https://adventofcode.com/2022/day/2
from __future__ import print_function
from pathlib import Path

# A == Rock (1)
# B == Paper (2)
# C == Scissors (3)
value = {'A': 1, 'B': 2, 'C': 3}

# piece -> (wins, loses)
game_win_lose = {
    'A': ('B', 'C'),
    'B': ('C', 'A'),
    'C': ('A', 'B')
}


def game_result(left, right):
    ret = value[right]
    if left == right:
        return 3 + ret
    win, _ = game_win_lose[left]
    return 6 + ret if right == win else ret


def part1(left, right):
    if right == 'X':
        return 'A'
    if right == 'Y':
        return 'B'
    if right == 'Z':
        return 'C'


def part2(left, code):
    if code == 'Y':
        return left
    win, lose = game_win_lose[left]
    return lose if code == 'X' else win


def game_total(data, eval_code):
    total = 0
    for round in data:
        left, right = round
        total += game_result(left, eval_code(left, right))
    return total


def process(data):
    # part 1
    result = game_total(data, part1)
    print("part 1:", result)
    # part 2
    result = game_total(data, part2)
    print("part 2:", result)


def parse_line(line):
    t = tuple(line.strip().split())
    assert t[0] in 'ABC'
    assert t[1] in 'XYZ'
    return t


def load_data(fileobj):
    return [parse_line(line) for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    main("test.txt")
    main()
