# http://adventofcode.com/2015/day/5
from __future__ import print_function
from enum import Enum
import re


class Command(Enum):
    turnon = 0
    turnoff = 1
    toggle = 2


ops1 = {Command.turnon: lambda val: 1,
        Command.turnoff: lambda val: 0,
        Command.toggle: lambda val: 1 - val}

ops2 = {Command.turnon: lambda val: val + 1,
        Command.turnoff: lambda val: val - 1 if val > 0 else 0,
        Command.toggle: lambda val: val + 2}


def apply(grid, func, start, to):
    for y in range(start[1], to[1]+1):
        row = grid[y]
        for x in range(start[0], to[0]+1):
            row[x] = func(row[x])
        grid[y] = row


WIDTH, HEIGHT = 1000, 10000


def count_lights(data, ops):
    grid = [[0] * WIDTH for _ in range(HEIGHT)]
    for command in data:
        op, start, to = command
        apply(grid, ops[op], start, to)
    result = sum(sum(row) for row in grid)
    return result


def process(data):
    # part 1
    print("part 1:", count_lights(data, ops1))
    # part 2
    print("part 2:", count_lights(data, ops2))


command_re = re.compile(
    r'(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)$')


def parse_line(line):
    match = command_re.match(line)
    assert match is not None, f"Failed to parse '{line}''"
    cmd = match.group(1)
    if cmd == "turn on":
        op = Command.turnon
    elif cmd == "turn off":
        op = Command.turnoff
    elif cmd == "toggle":
        op = Command.toggle
    else:
        assert False, f"Unknown command '{cmd}''"
    return op, (int(match.group(2)), int(match.group(3))), (int(match.group(4)), int(match.group(5)))


def load_data(fileobj):
    return [parse_line(line) for line in fileobj]


def main(file):
    print(file)
    with open(file) as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main("input.txt")
