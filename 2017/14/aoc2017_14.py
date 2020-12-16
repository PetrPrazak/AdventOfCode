# http://adventofcode.com/2017/day/14
from __future__ import print_function
from functools import reduce


# from ../Day10/aoc_day10 import knot_hash


def rotate(ring, pos, count):
    """ rotate partial list in ring from position pos for length count"""
    size = len(ring)
    for i in range(count // 2):
        start = (pos + i) % size
        end = (pos + count - 1 - i) % size
        ring[end], ring[start] = ring[start], ring[end]


def knot_hash_data(data, size):
    ring = list(range(size))
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


def knot_hash(data):
    ring = knot_hash_data(data, 256)
    out = []
    for block in range(16):
        out.append(reduce(lambda x, y: x ^ y,
                          ring[block * 16:block * 16 + 16]))
    khash = "".join("{:02x}".format(x) for x in out)
    return khash


def solve(pwd):
    print("Password:", pwd)
    total = 0
    grid = []
    for line in range(128):
        khash = knot_hash(pwd + '-' + str(line))
        bins = "".join([bin(int(x, 16))[2:].rjust(4, '0')
                        for x in list(khash)])
        total += bins.count("1")
        grid.append(list(bins))

    print("Total squares used:", total)
    # print_grid(grid)
    fill_regions(grid)
    # print_grid(grid)


def print_grid(grid):
    print()
    for row in grid:
        print("".join(row))


def fill_regions(grid):
    regions = 0
    for i in range(128):
        for j in range(128):
            if grid[i][j] == '1':
                regions += 1
                flood_fill(grid, i, j)
    print("Regions:", regions)


def flood_fill(grid, i, j):
    if grid[i][j] == '1':
        grid[i][j] = '#'
        if i > 0:
            flood_fill(grid, i - 1, j)
        if i < 127:
            flood_fill(grid, i + 1, j)
        if j > 0:
            flood_fill(grid, i, j - 1)
        if j < 127:
            flood_fill(grid, i, j + 1)


if __name__ == "__main__":
    # solve('flqrgnkx')
    solve('oundnydw')
    # solve('jxqlasbh')
