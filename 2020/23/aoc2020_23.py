# https://adventofcode.com/2020/day/23
from __future__ import print_function
from pprint import pprint
from pathlib import Path
from time import time


def game(cups, max_cup):
    current = cups[0]
    ex1 = cups[current]
    ex2 = cups[ex1]
    ex3 = cups[ex2]
    succ = current - 1
    while True:
        if succ <= 0:
            succ = max_cup
        if succ != ex1 and succ != ex2 and succ != ex3:
            break
        succ -= 1
    cups[current], cups[ex3], cups[succ] = cups[ex3], cups[succ], ex1
    cups[0] = cups[current]


def cycle(cups, max_cups, max_cycles=100):
    for _ in range(max_cycles):
        game(cups, max_cups)
    return cups


def init_cups(data):
    first, last = data[0], data[-1]
    cups = [0] * (len(data)+1)
    cups[0] = first
    for n, suc in zip(data, data[1:]):
        cups[n] = suc
    cups[last] = first
    return cups


def part1(cups):
    l = []
    x = 1
    while cups[x] != 1:
        x = cups[x]
        l.append(f"{x}")
    return ''.join(l)


def process(data):
    # part 1
    cups = init_cups(data)
    cycle(cups, max(data), max_cycles=100)
    print("part 1:", part1(cups))
    # part 2
    max_cups = 1000000
    data.extend(range(max(data)+1, max_cups + 1))
    assert len(data) == max_cups
    cups = init_cups(data)
    start = time()
    cycle(cups, max_cups, 10000000)
    duration = time() - start
    p1 = cups[1]
    p2 = cups[p1]
    result = p1 * p2
    print("part 2:", result, f"in {duration:.2f} seconds")


def load_data(fileobj):
    return list(int(c) for c in fileobj.read().rstrip())


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    main("test.txt")
    main()
