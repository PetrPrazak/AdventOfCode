from __future__ import print_function
from collections import Counter, defaultdict
from copy import deepcopy
from math import gcd, asin, sqrt, pi

cat = ''.join

INPUT = "aoc2019_10_input.txt"
TEST = "test.txt"


def read_input_lines(filename):
    with open(filename) as f:
        data = [list(l.rstrip()) for l in f.readlines()]
        return data


# return positions in range of `count` sorted by distance from `n`th position
def scanlines(count, n):
    l = list(range(count))
    tail = l[:n]
    if not tail:
        tail = []
    tail.reverse()
    return l[n:] + tail


def print_grid(grid):
    for row in grid:
        print(cat(row))


def count_positions(grid):
    width = len(grid[0])
    height = len(grid)
    out = [count_position(grid, width, height, (x, y))
           for y, row in enumerate(grid)
           for x, c in enumerate(row)
           if c is '#']
    return max(out)


def count_position(grid, width, height, pos):
    g = deepcopy(grid)
    check_position(g, width, height, pos)
    count = count_asteroids(g) - 1
    return count, pos


def check_position(grid, width, height, pos):
    x, y = pos
    lines = scanlines(height, y)
    cols = scanlines(width, x)
    for line in lines:
        for col in cols:
            cast_ray(grid, pos, col, line)


def cast_ray(grid, pos, col, line):
    x, y = pos
    if line == y and col == x:
        return
    pixel = grid[line][col]
    if pixel != '#':
        return
    dif_x, dif_y = get_ray_step(x, y, col, line)
    remove_blocked(grid, line, col, dif_y, dif_x)


# compute the angle of the ray from the point (x,y) to (col, line)
# in the form of steps
def get_ray_step(x, y, col, line):
    def sign(num):
        return -1 if num < 0 else 1

    dif_x = col - x
    dif_y = line - y
    d = gcd(dif_y, dif_x)
    dif_x = dif_x // d
    dif_y = dif_y // d
    if dif_y == 0:
        dif_x = sign(dif_x)
    elif dif_x == 0:
        dif_y = sign(dif_y)
    elif abs(dif_x) == abs(dif_y):
        dif_x = sign(dif_x)
        dif_y = sign(dif_y)
    return dif_x, dif_y


# remove asteroids blocked in particular direction
# the first run is the visible asteroid that should stay
def remove_blocked(grid, line, col, dif_y, dif_x, behind=False):
    if not ((0 <= line < len(grid)) and (0 <= col < len(grid[0]))):
        return
    if behind and grid[line][col] == '#':
        grid[line][col] = 'x'
    remove_blocked(grid, line + dif_y, col + dif_x, dif_y, dif_x, True)


def count_asteroids(grid):
    c = Counter()
    for row in grid:
        c += Counter(row)
    return c['#']


def make_dict(data):
    grid = {(x, y): c
            for (y, row) in enumerate(data)
            for (x, c) in enumerate(row)
            if c == '#'}
    return grid


# computes the angle of the line starting from North clockwise round the circle
def get_angle(dx, dy):
    angle = asin(dx / sqrt(dx * dx + dy * dy))
    if dy > 0:
        angle = pi - angle
    elif dx < 0:
        angle = 2 * pi + angle
    return angle


# computes the lists of visible asteroids
# returns a dictionary for every possible angle
# where the list is ordered by the distance from start position
def count_angles(grid, startx, starty):
    asteroids = defaultdict(list)
    for (x, y) in grid.keys():
        if y == starty and x == startx:
            continue
        dx, dy = get_ray_step(startx, starty, x, y)
        angle = get_angle(dx, dy)
        asteroids[angle].append((x, y))
    for angle in asteroids.keys():
        asteroids[angle].sort(key=lambda key: startx - key[0] + starty - key[1])
    return asteroids


# cycle in angles removing first in the list of positions
def part2(data, pos):
    grid = make_dict(data)
    allangles = count_angles(grid, pos[0], pos[1])
    winner = None
    order = 1
    while allangles:
        angles = list(sorted(allangles.keys()))
        for a in angles:
            asteroids = allangles[a]
            if not asteroids:
                del allangles[a]
                continue
            pos = asteroids.pop(0)
            # print(order, pos)
            if order == 200:
                winner = (100 * pos[0] + pos[1])
            order += 1
    return winner


def test1():
    data = read_input_lines(TEST)
    grid = deepcopy(data)
    width = len(grid[0])
    height = len(grid)
    print(count_position(grid, width, height, (11, 13)))


def test2():
    data = read_input_lines(TEST)
    print(part2(data, (11, 13)))


def main():
    data = read_input_lines(INPUT)
    max_ast, pos = count_positions(data)
    print(max_ast)  # 303
    w = part2(data, pos)
    print(w)  # 408


if __name__ == '__main__':
    main()
    # test2()
