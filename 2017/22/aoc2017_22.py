# http://adventofcode.com/2017/day/22
from __future__ import print_function
from collections import defaultdict


def solve(lines):
    inp = [list(line.strip()) for line in lines]
    grid = defaultdict(lambda: '.')
    for i, l in enumerate(inp):
        for j in range(len(inp[i])):
            grid[(j, i)] = l[j]

    starty = len(inp) // 2
    startx = len(inp[starty]) // 2

    states = ['.', '#']
    rotations = [3, 1]
    walk(startx, starty, grid.copy(), states, rotations, 10000)

    states = ['.', 'W', '#', 'F']
    rotations = [3, 0, 1, 2]
    walk(startx, starty, grid.copy(), states, rotations, 10000000)


# increments of coordinates for each direction
# UP, RIGHT, DOWN, LEFT
dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def walk(x, y, grid, states, rotations, reps):
    d = 0  # Up
    count = 0
    for _ in range(reps):
        node = grid[(x, y)]
        idx = states.index(node)
        nextstate = states[(idx + 1) % len(states)]
        grid[(x, y)] = nextstate
        d = (d + rotations[idx]) % 4
        dx, dy = dirs[d]
        x, y = x + dx, y + dy
        if nextstate == '#':
            count += 1

    print(count)


def main():
    with open("input.txt") as f:
        lines = f.readlines()
        solve(lines)


if __name__ == "__main__":
    main()
