# https://adventofcode.com/2020/day/14
from __future__ import print_function
from collections import defaultdict


def parse_mask(line):
    return [2 ** i * (1 if b == '1' else -1)
            for i, b in enumerate(reversed(line))
            if b != 'X']


def masked(val, mask):
    for m in mask:
        if m > 0:
            val |= m
        else:
            val &= m - 1
    return val


def part1(data):
    mask = []
    mem = defaultdict(int)
    for addr, val in data:
        if addr is None:
            mask = parse_mask(val)
        else:
            mem[addr] = masked(val, mask)
    return mem


def parse_mem_mask(line):
    ones = [2 ** i for i, b in enumerate(reversed(line))
            if b == '1']
    floats = [2 ** i for i, b in enumerate(reversed(line))
              if b == 'X']
    return ones, floats


def print_bits(addr):
    print(format(addr, "b"), addr)


def apply_masks(mem, addr, val, mask):
    ones, floats = mask
    for o in ones:
        addr |= o
    for l in range(2 ** len(floats)):
        faddr = addr
        for bit, orig in enumerate(floats):
            if l & (2 ** bit) == 0:
                faddr &= ~orig
            else:
                faddr |= orig
        mem[faddr] = val


def part2(data):
    mask = ([], [])
    mem = defaultdict(int)
    for addr, val in data:
        if addr is None:
            mask = parse_mem_mask(val)
        else:
            apply_masks(mem, addr, val, mask)
    return mem


def process(data):
    # part 1
    mem = part1(data)
    result = sum(mem.values())
    print("part 1:", result)
    # part 2
    mem = part2(data)
    result = sum(mem.values())
    print("part 2:", result)


def parse_line(line):
    l, r = line.split(' = ')
    if l == 'mask':
        return None, r
    else:
        idx = l.find(']')
        return int(l[4:idx]), int(r)


def load_data(fileobj):
    return [parse_line(line.rstrip()) for line in fileobj]


def main(file):
    print(file)
    with open(file) as f:
        process(load_data(f))


if __name__ == "__main__":
    main("test.txt")
    main("input.txt")
