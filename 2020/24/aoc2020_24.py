# https://adventofcode.com/2020/day/24
from __future__ import print_function
from pprint import pprint
from pathlib import Path
from itertools import product

# https://www.redblobgames.com/grids/hexagons/


def gridwalk(steps):
    x, y, z = 0, 0, 0
    for s in steps:
        if s == 'e' or s == 'w':
            inc = 1 if s == 'w' else -1
            x -= inc
            y += inc
        elif s == 'ne' or s == 'sw':
            inc = 1 if s == 'ne' else -1
            x += inc
            z -= inc
        elif s == 'se' or s == 'nw':
            inc = 1 if s == 'se' else -1
            y -= inc
            z += inc
    return x, y, z


all_tiles = [(x, y, z) for x, y, z in product([-1, 0, 1], repeat=3)
             if x+y+z == 0]
neighbors = all_tiles[:]
neighbors.remove((0, 0, 0))


def sum_neighbors(blacks, pos):
    x, y, z = pos
    return sum(bool((x+dx, y+dy, z+dz) in blacks) for dx, dy, dz in neighbors)


def get_new_color(colors, pos, val):
    num_blacks = sum_neighbors(colors, pos)
    if not val and num_blacks == 2:
        val = True
    elif val and (num_blacks == 0 or num_blacks > 2):
        val = False
    return val


def new_blacks(blacks):
    newblacks = set()
    for pos in blacks:
        x, y, z = pos
        for dx, dy, dz in all_tiles:
            newpos = x+dx, y+dy, z+dz
            if get_new_color(blacks, newpos, newpos in blacks):
                newblacks.add(newpos)
    return newblacks


def cycle(blacks, n=1):
    for _ in range(n):
        blacks = new_blacks(blacks)
    return blacks


def process(data):
    # part 1
    blacks = set()
    for line in data:
        pos = gridwalk(line)
        if pos in blacks:
            blacks.remove(pos)
        else:
            blacks.add(pos)
    result = len(blacks)
    print("part 1:", result)
    # part 2
    blacks = cycle(blacks, 100)
    result = len(blacks)
    print("part 2:", result)


def parse_line(line):
    out = []
    it = iter(line)
    for c in it:
        if c == 'w' or c == 'e':
            out.append(c)
        else:
            d = next(it)
            out.append(c + d)
    return out


def load_data(fileobj):
    return [parse_line(line.rstrip()) for line in fileobj]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    main("test.txt")
    main()
