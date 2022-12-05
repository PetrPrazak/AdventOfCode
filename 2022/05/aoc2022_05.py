# https://adventofcode.com/2022/day/5
from pathlib import Path
from copy import deepcopy
import re


def handle_moves(stacks, moves, part=1):
    stacks = deepcopy(stacks)
    for quantity, start, end in moves:
        stack_to_move = stacks[start-1][-quantity:]
        del stacks[start-1][-quantity:]
        if part == 1:
            stack_to_move = reversed(stack_to_move)
        stacks[end-1].extend(stack_to_move)
 
    return ''.join(s[-1] for s in stacks)


def process(data):
    # part 1
    result = handle_moves(*data, part=1)
    print("part 1:", result)
    # part 2
    result = handle_moves(*data, part=2)
    print("part 2:", result)


def rotate_lines(lines):
    return [''.join(reversed(r)) for r in zip(*lines)]


def parse_stacks(section):
    lines = rotate_lines(section.split('\n'))
    return [list(line.rstrip()[1:]) for line in lines if line[0].isdigit()]


def parse_moves(section):
    return [tuple(map(int, re.findall('\d+', line))) for line in section.rstrip().split('\n')]


def load_data(fileobj):
    stacks, moves = fileobj.read().split("\n\n")
    return parse_stacks(stacks), parse_moves(moves)


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    main("test.txt")
    main()
