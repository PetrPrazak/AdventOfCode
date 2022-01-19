# https://adventofcode.com/2018/day/20
from __future__ import print_function
from pathlib import Path
from math import inf


def parse(regex):
    pos = 0, 0
    dist = 0
    pos_stack = []
    rooms = dict()
    for char in regex:
        if char in 'NSWE':
            if char == 'N':
                pos = pos[0], pos[1] - 1
            elif char == 'S':
                pos = pos[0], pos[1] + 1
            elif char == 'W':
                pos = pos[0] - 1, pos[1]
            elif char == 'E':
                pos = pos[0] + 1, pos[1]
            dist += 1
            rooms[pos] = min(rooms.get(pos, inf), dist)
        elif char == '(':
            pos_stack.append((pos, dist))
        elif char == ')':
            pos, dist = pos_stack.pop()
        elif char == '|':
            pos, dist = pos_stack[-1]
    return rooms


def process(data):
    rooms = parse(data[1:-1])
    # part 1
    result = max(rooms.values())
    print("part 1:", result)
    # part 2
    result = sum(d >= 1000 for d in rooms.values())
    print("part 2:", result)


def load_data(fileobj):
    return fileobj.read().strip()


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
