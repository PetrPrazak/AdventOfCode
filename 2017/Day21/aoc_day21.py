"""

http://adventofcode.com/2017/day/21

"""
from __future__ import print_function
from collections import defaultdict, Counter

"""
AB   CA   DC   BD
CD   DB   BA   AC
"""

rot2 = [(0, 1, 2, 3), (2, 0, 3, 1), (3, 2, 1, 0), (1, 3, 0, 2)]

"""
AB   BA   CD
CD   DC   AB
"""
flip2 = [(0, 1, 2, 3), (1, 0, 3, 2), (2, 3, 0, 1)]

"""
ABC  GDA   IHG   CFI
DEF  HEB   FED   BEH
GHI  IFC   CBA   ADG

"""

rot3 = [(0, 1, 2, 3, 4, 5, 6, 7, 8),
        (6, 3, 0, 7, 4, 1, 8, 5, 2),
        (8, 7, 6, 5, 4, 3, 2, 1, 0),
        (2, 5, 8, 1, 4, 7, 0, 3, 6)]

"""
ABC   CBA   GHI
DEF   FED   DEF
GHI   IHG   ABC

"""
flip3 = [(0, 1, 2, 3, 4, 5, 6, 7, 8),
         (2, 1, 0, 5, 4, 3, 8, 7, 6),
         (6, 7, 8, 3, 4, 5, 0, 1, 2)]


def enumgrid(grid):
    size = len(grid)
    if size % 2 == 0:
        blocks = size // 2
        for x in range(blocks):
            for y in range(blocks):
                a, b = x * 2, y * 2
                subgrid = "".join(grid[a + x][b + y] for x in range(2) for y in range(2))
                yield x, y, subgrid

    elif size % 3 == 0:
        blocks = size // 3
        for x in range(blocks):
            for y in range(blocks):
                a, b = x * 3, y * 3
                subgrid = "".join(grid[a + x][b + y] for x in range(3) for y in range(3))
                yield x, y, subgrid
    else:
        raise ValueError("grid not divisible by 2 or 3")


def parse_input(lines):
    mappings = dict()
    for line in lines:
        part = line.strip().split(" => ")
        match = part[0].replace('/', '')
        if len(match) == 4:  # 2x2
            for f in flip2:
                flip = "".join(match[f[x]] for x in range(4))
                for r in rot2:
                    s = "".join(flip[r[x]] for x in range(4))
                    mappings[s] = part[1]
        elif len(match) == 9:  # 3x3
            for f in flip3:
                flip = "".join(match[f[x]] for x in range(9))
                for r in rot3:
                    s = "".join(flip[r[x]] for x in range(9))
                    mappings[s] = part[1]
    return mappings


def solve(lines):
    mappings = parse_input(lines)

    for part, rep in enumerate([5, 18]):
        # start position
        grid = [".#.", "..#", "###"]
        for _ in range(rep):
            newgrid = defaultdict(str)
            for x, y, subgrid in enumgrid(grid):
                if subgrid in mappings:
                    newsubgrid = mappings[subgrid].split('/')
                    for l, s in enumerate(newsubgrid):
                        newgrid[x * len(newsubgrid) + l] += s
                else:
                    print("Subgrid not found!", subgrid)

            if newgrid:
                grid = []
                for l in sorted(newgrid.keys()):
                    grid.append(newgrid[l])

        # count hash signs
        c = Counter()
        for r in grid:
            c.update(r)
        print(part + 1, c['#'])


INPUT = "aoc_day21_input.txt"
# INPUT = "aoc_day21_test.txt"


def main():
    with open(INPUT) as f:
        # read by lines
        lines = f.readlines()
        solve(lines)


if __name__ == "__main__":
    main()
