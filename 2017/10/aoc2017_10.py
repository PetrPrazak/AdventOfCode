
# http://adventofcode.com/2017/day/10
from __future__ import print_function
from functools import reduce


def rotate(ring, pos, count):
    """ rotate partial list in ring from position pos for length count"""
    size = len(ring)
    for i in range(count // 2):
        start = (pos + i) % size
        end = (pos + count - 1 - i) % size
        ring[end], ring[start] = ring[start], ring[end]


def knot_hash(data, size, part):

    ring = list(range(size))
    if part == 1:
        items = [int(x) for x in data.split(',')]
        repeat = 1
    else:
        assert size % 16 == 0
        items = [ord(x) for x in list(data)] + [17, 31, 73, 47, 23]
        repeat = 64

    skip = 0
    pos = 0
    for _ in range(repeat):
        for n in items:
            if n > 1:
                rotate(ring, pos, n)
            pos = (pos + n + skip) % size
            skip += 1

    return ring


def solve(data, size, part=1):
    khash = knot_hash(data, size, part)
    if part == 1:
        print(khash[0] * khash[1])
    else:
        out = []
        for block in range(size // 16):
            out.append(reduce(lambda x, y: x ^ y, khash[block*16:block*16+16]))
        print("".join("{:02x}".format(x) for x in out))


if __name__ == "__main__":
    # test cases
    solve("3,4,1,5", 5)      # result == 12
    solve("", 256, 2)        # result == a2582a3a0e66e6e86e3812dcb672a272

    with open("input.txt") as f:
        data = f.read().strip()
        solve(data, 256)
        solve(data, 256, 2)
