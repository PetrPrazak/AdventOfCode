# https://adventofcode.com/2020/day/5
from __future__ import print_function

trans_table = str.maketrans("FBLR", "0101")


def get_id(board_pass):
    return int(board_pass.translate(trans_table), 2)


def eliminate(seats):
    missing = set(range(min(seats), max(seats))) - seats
    return missing


def process(data):
    # part 1
    seats = {get_id(bp) for bp in data}
    print("part 1:", max(seats))
    # part 2
    myid = eliminate(seats)
    print("part 2:", myid.pop())


def load_data(fileobj):
    return [line.strip() for line in fileobj]


def main(file):
    print(file)
    with open(file) as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main("input.txt")
