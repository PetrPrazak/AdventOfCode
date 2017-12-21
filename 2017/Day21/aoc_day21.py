"""

http://adventofcode.com/2017/day/21

"""
from __future__ import print_function
from collections import defaultdict, Counter

"""
AB   CA   DC    BD
CD   DB   BA    AC
"""

rot2 = [(0, 1, 2, 3), (2, 0, 3, 1), (3, 2, 1, 0), (1, 3, 0, 2)]

"""
AB  BA  CD
CD  DC  AB
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


def solve(lines):
    mappings = dict()
    for line in lines:
        part = line.strip().split(" => ")
        match = part[0]
        if len(match) == 5:  # 2x2
            match = match.replace('/', '')
            for f in flip2:
                flip = "".join(match[f[x]] for x in range(4))
                for r in rot2:
                    s = "".join(flip[r[x]] for x in range(4))
                    s = s[0:2] + '/' + s[2:]
                    mappings[s] = part[1]

        elif len(match) == 11:  # 3x3
            match = match.replace('/', '')
            for f in flip3:
                flip = "".join(match[f[x]] for x in range(9))
                for r in rot3:
                    s = "".join(flip[r[x]] for x in range(9))
                    s = s[0:3] + '/' + s[3:6] + '/' + s[6:]
                    mappings[s] = part[1]

    for part, rep in enumerate([5,18]):
        # start position
        grid = [".#.", "..#", "###"]
        for _ in range(rep):
            newgrid = defaultdict(str)

            if len(grid) % 2 == 0:
                for x in range(len(grid) // 2):
                    for y in range(len(grid[0]) // 2):
                        a, b = (x * 2, y * 2)

                        subgrid = grid[a][b] + grid[a][b + 1] + '/' + grid[a + 1][b] + grid[a + 1][b + 1]
                        if subgrid in mappings:
                            newsubgrid = mappings[subgrid]
                            for l, s in enumerate(newsubgrid.split('/')):
                                newgrid[x * 3 + l] += s
                        else:
                            print("Subgrid not found", subgrid)

            elif len(grid) % 3 == 0:
                for x in range(len(grid) // 3):
                    for y in range(len(grid[0]) // 3):
                        a, b = (x * 3, y * 3)
                        subgrid = grid[a][b] + grid[a][b + 1] + grid[a][b + 2] + '/' \
                                  + grid[a + 1][b] + grid[a + 1][b + 1] + grid[a + 1][b + 2] + '/' \
                                  + grid[a + 2][b] + grid[a + 2][b + 1] + grid[a + 2][b + 2]
                        if subgrid in mappings:
                            newsubgrid = mappings[subgrid]
                            for l, s in enumerate(newsubgrid.split('/')):
                                newgrid[x * 4 + l] += s
                        else:
                            print("Subgrid not found", subgrid)
            else:
                print("not divisible by 2 or 3!")

            if newgrid:
                grid = []
                for l in sorted(newgrid.keys()):
                    grid.append(newgrid[l])

            # print("Grid:")
            # for s in grid:
            #     print(s)
            # print()

        print(part+1, Counter("".join(grid))['#'])


INPUT = "aoc_day21_input.txt"
# INPUT = "aoc_day21_test.txt"


def main():
    with open(INPUT) as f:
        # read by lines
        lines = f.readlines()
        solve(lines)


if __name__ == "__main__":
    main()
