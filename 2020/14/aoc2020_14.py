# https://adventofcode.com/2020/day/14
from __future__ import print_function


def parse_mask(line):
    return [2 ** i * (1 if b == '1' else -1)
            for i, b in enumerate(reversed(line))
            if b != 'X']


def masked(val, mask):
    for m in mask:
        if m > 0:
            val |= m
        else:
            val &= m - 1   # already negative -> turn to 2'complement
    return val


def part1(data):
    mask = []
    mem = dict()
    for addr, val in data:
        if addr is None:
            mask = parse_mask(val)
        else:
            mem[addr] = masked(val, mask)
    return mem


def parse_mem_mask(line):
    ones = [2 ** i for i, b in enumerate(reversed(line)) if b == '1']
    floats = [2 ** i for i, b in enumerate(reversed(line)) if b == 'X']
    return ones, floats


def apply_masks(mem, addr, val, masks):
    ones, floats = masks
    for o in ones:
        addr |= o
    for flt in range(2 ** len(floats)):
        faddr = addr
        for bit, orig_bit in enumerate(floats):
            if flt & (2 ** bit) == 0:
                faddr &= ~orig_bit
            else:
                faddr |= orig_bit
        mem[faddr] = val


def part2(data):
    masks = ([], [])
    mem = dict()
    for addr, val in data:
        if addr is None:
            masks = parse_mem_mask(val)
        else:
            apply_masks(mem, addr, val, masks)
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
        idx = l.find(']')  # mem[xxx]
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
