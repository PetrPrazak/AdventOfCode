# http://adventofcode.com/2016/day/2
from __future__ import print_function


def get_new_pos(pos, dir):
    x, y = pos
    if dir == 'U':
        if y > 0: y -= 1
    elif dir == 'D':
        if y < 2: y += 1
    elif dir == 'L':
        if x > 0: x -= 1
    elif dir == 'R':
        if x < 2: x += 1
    return x, y


def walk_positions(pos, instructions):
    for dir in instructions:
        pos = get_new_pos(pos, dir)
    return pos


def solve1(line):
    grid = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
    pos = (1, 1)
    ans = list()
    for line in lines:
        pos = walk_positions(pos, line)
        x, y = pos
        ans.append(grid[y][x])
    print("".join(ans))


def get_new_pos2(pos, dir):
    x, y = pos
    if dir == 'U':
        if y > 0: y -= 1
    elif dir == 'D':
        if y < 4: y += 1
    elif dir == 'L':
        if x > 0: x -= 1
    elif dir == 'R':
        if x < 4: x += 1
    return x, y


def solve2(line):
    grid = [[' ', ' ', '1', ' ', ' '],
            [' ', '2', '3', '4', ' '],
            ['5', '6', '7', '8', '9'],
            [' ', 'A', 'B', 'C', ' '],
            [' ', ' ', 'D', ' ', ' ']]

    pos = (0, 2)
    ans = list()
    for line in lines:
        for dir in line:
            newpos = get_new_pos2(pos, dir)
            x, y = newpos
            if grid[y][x] != ' ':
                pos = newpos
        x, y = pos
        ans.append(grid[y][x])
    print("".join(ans))


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = [l.strip() for l in f.readlines()]
        solve1(lines)
        solve2(lines)
