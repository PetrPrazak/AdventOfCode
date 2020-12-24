# https://adventofcode.com/2020/day/24
from __future__ import print_function
from pprint import pprint
from pathlib import Path
from itertools import product

# https://www.redblobgames.com/grids/hexagons/

DIFFS = { "e": (1, -1, 0),
          "w": (-1, 1, 0),
         "nw": ( 0, 1,-1),
         "se": ( 0,-1, 1),
         "ne": ( 1, 0,-1),
         "sw": (-1, 0, 1)}


def gridwalk(steps):
    x, y, z = 0, 0, 0
    for s in steps:
        dx, dy, dz = DIFFS[s]
        x, y, z = x + dx, y + dy, z + dz
    return x, y, z


all_tiles = [(x, y, z) for x, y, z in product([-1, 0, 1], repeat=3)
             if x+y+z == 0]
neighbors = all_tiles[:]
neighbors.remove((0, 0, 0))


def sum_neighbors(blacks, pos):
    x, y, z = pos
    return sum(bool((x+dx, y+dy, z+dz) in blacks) for dx, dy, dz in neighbors)


def turn_to_black(colors, pos, is_black):
    num_blacks = sum_neighbors(colors, pos)
    if not is_black and num_blacks == 2:
        is_black = True
    elif is_black and (num_blacks == 0 or num_blacks > 2):
        is_black = False
    return is_black


def get_all_neighbors(pos):
    x, y, z = pos
    for dx, dy, dz in all_tiles:
        yield x+dx, y+dy, z+dz


def new_blacks(blacks):
    newblacks = set()
    for pos in blacks:
        for newpos in get_all_neighbors(pos):
            if turn_to_black(blacks, newpos, newpos in blacks):
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
        blacks ^= {pos}
    result = len(blacks)
    print("part 1:", result)
    # part 2
    blacks = cycle(blacks, 100)
    result = len(blacks)
    print("part 2:", result)


def parse_line(line):
    return line.replace("e", "e ").replace("w", "w ").rstrip().split(" ")


def load_data(fileobj):
    return [parse_line(line) for line in fileobj]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    main("test.txt")
    main()
