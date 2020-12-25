# https://adventofcode.com/2020/day/25
from __future__ import print_function

m = 20201227

def calc_secret(public_key):
    loops = 0
    value = 1
    while value != public_key:
        loops += 1
        value = (7 * value) % m
    return loops


def process(data):
    pk1, pk2 = data
    # part 1
    loops1 = calc_secret(pk1)
    # loops2 = calc_secret(pk2)
    result = pow(pk2, loops1, m)
    # assert result == pow(pk1, loops2, m)
    print("part 1:", result)


def load_data(fileobj):
    return [int(line) for line in fileobj.readlines()]


def main(file):
    print(file)
    with open(file) as f:
        process(load_data(f))


if __name__ == "__main__":
    main("test.txt")
    main("input.txt")
