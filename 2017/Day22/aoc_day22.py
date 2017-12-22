"""

http://adventofcode.com/2017/day/22


"""
from __future__ import print_function
from collections import defaultdict


def solve(lines):
    part1(lines)
    part2(lines)


def part1(lines):
    total = 0
    inp = [list(line.strip()) for line in lines]
    # print(inp)
    grid = defaultdict(lambda: '.')
    for i, l in enumerate(inp):
        for j, node in enumerate(inp[i]):
            grid[(j, i)] = l[j]

    # print(grid)
    y = (len(inp) + 1) // 2 - 1
    x = (len(inp[y]) + 1) // 2 - 1

    d = 0
    dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    states = ['.', 'W', 'I', 'F']
    dirtext = ['U', 'R', 'D', 'L']

    count = 0
    for _ in range(10000):

        node = grid[(x, y)]
        if node == '.':
            count += 1
            grid[(x, y)] = '#'
            d = (d - 1) % 4
        else:
            grid[(x, y)] = '.'
            d = (d + 1) % 4

        # print(x,y,node, dirtext[d])
        dx, dy = dirs[d]
        x, y = x + dx, y + dy

    print(count)


def part2(lines):
    inp = [list(line.strip()) for line in lines]
    grid = defaultdict(int)
    for i, l in enumerate(inp):
        for j, node in enumerate(inp[i]):
            grid[(j, i)] = 0 if l[j] == '.' else 2

    y = (len(inp) + 1) // 2 - 1
    x = (len(inp[y]) + 1) // 2 - 1

    d = 0
    dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    states = ['.', 'W', 'I', 'F']
    dirtext = ['U', 'R', 'D', 'L']

    count = 0
    for _ in range(10000000):

        node = grid[(x, y)]
        if node == 0:
            d = (d + 3) % 4
        elif node == 1:
            count += 1
            pass
        elif node == 2:
            d = (d + 1) % 4
        elif node == 3:
            d = (d + 2) % 4

        grid[(x, y)] = (node + 1) % 4
        # print(x, y, states[node], dirtext[d])
        dx, dy = dirs[d]
        x, y = x + dx, y + dy

    print(count)


INPUT = "aoc_day22_input.txt"
# INPUT = "aoc_day22_test.txt"


def main():
    with open(INPUT) as f:
        # read all in once
        # data = f.read()
        # solve(data)
        # read by lines
        lines = f.readlines()
        solve(lines)


if __name__ == "__main__":
    main()
