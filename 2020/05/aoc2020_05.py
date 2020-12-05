# https://adventofcode.com/2020/day/5
from __future__ import print_function


def split(low, start, end):
    mid, _ = divmod(end + 1 + start, 2)
    return (start, mid - 1) if low else (mid, end)


def find_seat(instructions, low_dir, max_val):
    interval = (0, max_val)
    for d in instructions:
        low = d == low_dir
        interval = split(low, *interval)
    return interval[0]


def get_id(board_pass):
    row = find_seat(board_pass[:7], 'F', 127)
    col = find_seat(board_pass[7:], 'L', 7)
    return row * 8 + col


def eliminate(seats):
    max_id = 127*8+7
    missing = set(range(max_id + 1)) - set(seats)
    low_bound = 0
    while low_bound in missing:
        low_bound += 1
    high_bound = max_id
    while high_bound in missing:
        high_bound -= 1
    myid = missing - set(range(low_bound)) - set(range(high_bound+1, max_id+1))
    return myid


def process(data):
    # part 1
    seats = [get_id(bp) for bp in data]
    print("part 1:", max(seats))
    # part 2
    myid = eliminate(seats)
    result = myid.pop()
    print("part 2:", result)


def load_data(fileobj):
    return [line.strip() for line in fileobj]


def main(file):
    print(file)
    with open(file) as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main("input.txt")
