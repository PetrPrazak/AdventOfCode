# https://adventofcode.com/2016/day/18
from __future__ import print_function
from pathlib import Path

TRAP = '^'
EMPTY = '.'


def new_tile(left, right):
    """
    Its left and center tiles are traps, but its right tile is not.
    Its center and right tiles are traps, but its left tile is not.
    Only its left tile is a trap.
    Only its right tile is a trap.

    Actually, the outcome doesn't rely on the center tile at all..."""
    return TRAP if left != right else EMPTY


def count_empty(seed, rows):
    row_len = len(seed)
    result = seed.count(EMPTY)
    line = list(seed)
    for _ in range(1, rows):
        line = [EMPTY] + line + [EMPTY]
        line = [new_tile(line[t-1], line[t+1]) for t in range(1, row_len+1)]
        result += line.count(EMPTY)
    return result


def process(data):
    rows = 40 if len(data) > 10 else 10
    result = count_empty(data, rows)
    print("part 1:", result)
    # part 2
    result = count_empty(data, 400000)
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
